import asyncio
import os
import secrets
from datetime import datetime
from typing import Any

import magic
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError  # pylint: disable=import-error
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

import uuid
from app.core.database import get_db
from app.core.security import get_api_key
from app.models.claims import Claim, ClaimPhoto
from app.schemas.claims import ClaimCreate, ClaimPhotoResponse, ClaimResponse
from app.services.storage import storage_service
from app.services.ai_service import ai_service
from app.services.adjudication_service import adjudication_service
from app.services.email import email_service

router = APIRouter()

# Security constants for file uploads
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}


@router.post("/", response_model=ClaimResponse, dependencies=[Depends(get_api_key)])
async def create_claim(
    claim_in: ClaimCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create a new claim.
    """
    # Format: CLM-YYYY-001234
    claim_number = (
        f"CLM-{datetime.now().year}-{str(secrets.randbelow(1000000)).zfill(6)}"
    )

    new_claim = Claim(
        policy_number=claim_in.policy_number,
        claim_number=claim_number,
        incident_date=claim_in.incident_date,
        incident_location=claim_in.incident_location,
        incident_description=claim_in.incident_description,
        vehicle_vin=claim_in.vehicle_vin,
        vehicle_make=claim_in.vehicle_make,
        vehicle_model=claim_in.vehicle_model,
        vehicle_year=claim_in.vehicle_year,
        claimant_name=claim_in.claimant_name,
        claimant_email=claim_in.claimant_email,
        claimant_phone=claim_in.claimant_phone,
        status="New",
    )

    db.add(new_claim)
    await db.commit()
    await db.refresh(new_claim)

    # Needs to fetch relations eagerly since response_model requires it
    # We'll re-fetch the claim using selectinload to avoid MissingGreenlet
    stmt = (
        select(Claim)
        .where(Claim.id == new_claim.id)
        .options(selectinload(Claim.photos))
    )
    result = await db.execute(stmt)
    new_claim_with_rels = result.scalars().first()

    return new_claim_with_rels


@router.get(
    "/{claim_id}", response_model=ClaimResponse, dependencies=[Depends(get_api_key)]
)
async def get_claim(claim_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    """
    Get a claim by ID.
    """
    # Fetch claim with eager loading of photos to avoid async compatibility issues
    stmt = (
        select(Claim)
        .where(Claim.id == claim_id)
        .options(selectinload(Claim.photos))
    )
    result = await db.execute(stmt)
    claim = result.scalars().first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim

@router.get(
    "/lookup/{claim_number}", response_model=ClaimResponse
)
async def lookup_claim(claim_number: str, db: AsyncSession = Depends(get_db)) -> Any:
    """
    Lookup a claim by claim_number without API key (public).
    """
    stmt = (
        select(Claim)
        .where(Claim.claim_number == claim_number)
        .options(selectinload(Claim.photos))
    )
    result = await db.execute(stmt)
    claim = result.scalars().first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim


@router.post(
    "/{claim_id}/photos",
    response_model=ClaimPhotoResponse,
    dependencies=[Depends(get_api_key)],
)
async def upload_claim_photo(
    claim_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Upload a photo for a claim.
    """
    # 1. Validate File Content Type via magic bytes
    file_content = await file.read(2048)
    # Offload the synchronous python-magic call to a thread to prevent blocking the async event loop
    actual_mime_type = await asyncio.to_thread(
        magic.from_buffer, file_content, mime=True
    )
    await file.seek(0)

    if actual_mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file content type: {actual_mime_type}. Allowed types: {', '.join(ALLOWED_MIME_TYPES)}",
        )

    # 2. Validate File Extension (Strict enforcement to prevent unrestricted file upload)
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Security Policy Violation: Invalid file extension: {ext}. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Save file
    file_path = await storage_service.upload_file(file)

    # Create Photo Record
    new_photo = ClaimPhoto(
        claim_id=claim_id,
        photo_url=file_path,  # Storing local path as URL for now
        photo_type=file.content_type,
    )

    db.add(new_photo)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        # Clean up the orphaned file
        await storage_service.delete_file(file_path)
        raise HTTPException(status_code=404, detail="Claim not found") from exc

    await db.refresh(new_photo)

    return new_photo

@router.post(
    "/{claim_id}/analyze", dependencies=[Depends(get_api_key)]
)
async def analyze_claim(claim_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Trigger AI analysis on claim photos"""
    # Fetch claim with eager loading of photos to avoid redundant database calls
    stmt = select(Claim).where(Claim.id == claim_id).options(selectinload(Claim.photos))
    result = await db.execute(stmt)
    claim_with_photos = result.scalars().first()

    if not claim_with_photos:
        raise HTTPException(404, "Claim not found")

    if not claim_with_photos.photos:
        raise HTTPException(400, "No photos to analyze")

    # Get photo URLs
    photo_urls = [photo.photo_url for photo in claim_with_photos.photos]

    # Call AI service
    analysis = await ai_service.assess_damage(
        photo_urls=photo_urls,
        vehicle_info={
            "make": claim_with_photos.vehicle_make,
            "model": claim_with_photos.vehicle_model,
            "year": claim_with_photos.vehicle_year,
        },
        incident_info={
            "description": claim_with_photos.incident_description,
            "date": claim_with_photos.incident_date,
        }
    )

    # Update claim with AI results
    claim_with_photos.estimated_damage_cost = analysis["estimated_cost"]

    # Store AI analysis in photos
    for photo in claim_with_photos.photos:
        photo.ai_analysis = analysis

    # Mock Policy and Fraud Score since full external db isn't there
    mock_policy = {
        "status": "Active",
        "coverage_limit": 50000.0,
        "deductible": 500.0
    }

    mock_fraud_score = 0
    if claim_with_photos.estimated_damage_cost and float(claim_with_photos.estimated_damage_cost) > 10000:
        mock_fraud_score += 15

    # Trigger Auto-Adjudication
    claim_dict = {"estimated_damage_cost": claim_with_photos.estimated_damage_cost}
    adjudication_result = adjudication_service.evaluate_claim(
        claim=claim_dict,
        policy=mock_policy,
        ai_analysis=analysis,
        fraud_score=mock_fraud_score
    )

    new_status = adjudication_result["status"]
    claim_with_photos.status = new_status

    if new_status == "Approved":
        claim_with_photos.approved_amount = claim_with_photos.estimated_damage_cost
        email_body = f"Your claim {claim_with_photos.claim_number} has been automatically approved for ${claim_with_photos.approved_amount}!"
        await email_service.send_email(
            to=claim_with_photos.claimant_email,
            subject="Claim Approved",
            body=email_body
        )
    elif new_status == "Manual Review":
        email_body = f"Your claim {claim_with_photos.claim_number} is currently under manual review."
        await email_service.send_email(
            to=claim_with_photos.claimant_email,
            subject="Claim Under Review",
            body=email_body
        )

    await db.commit()

    return {"claim_id": claim_id, "analysis": analysis, "adjudication": adjudication_result}
