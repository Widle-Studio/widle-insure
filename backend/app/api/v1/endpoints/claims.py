import os
import secrets
import uuid
from datetime import datetime
from typing import Any

import magic
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_api_key
from app.models.claims import Claim, ClaimPhoto
from app.schemas.claims import ClaimCreate, ClaimPhotoResponse, ClaimResponse
from app.services.storage import storage_service

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
    result = await db.execute(select(Claim).where(Claim.id == claim_id))
    claim = result.scalars().first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    # Helper to fetch photos eagerly if needed, or rely on lazy loading (async compatibility issue potentially)
    # For now, let's assume simple access. If relationships fail in async, we need joinedload.
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
    # 1. Validate File Type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed types: {', '.join(ALLOWED_MIME_TYPES)}",
        )

    # 1.5 Validate file contents via python-magic
    file_content = await file.read(2048)
    actual_mime_type = magic.from_buffer(file_content, mime=True)
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

    # Check if claim exists
    result = await db.execute(select(Claim).where(Claim.id == claim_id))
    claim = result.scalars().first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    # Save file
    file_path = await storage_service.upload_file(file)

    # Create Photo Record
    new_photo = ClaimPhoto(
        claim_id=claim_id,
        photo_url=file_path,  # Storing local path as URL for now
        photo_type=file.content_type,
    )

    db.add(new_photo)
    await db.commit()
    await db.refresh(new_photo)

    return new_photo
