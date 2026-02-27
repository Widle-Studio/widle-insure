from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.claims import Claim, ClaimPhoto
from app.schemas.claims import ClaimCreate, ClaimResponse, ClaimPhotoResponse
from app.services.storage import storage_service
from app.core.security import get_api_key
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/", response_model=ClaimResponse, dependencies=[Depends(get_api_key)])
async def create_claim(
    claim_in: ClaimCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create a new claim.
    """
    claim_number = f"CLM-{datetime.now().year}-{uuid.uuid4().hex[:6].upper()}"
    
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
        status="New"
    )
    
    db.add(new_claim)
    await db.commit()
    await db.refresh(new_claim)
    return new_claim

@router.get("/{claim_id}", response_model=ClaimResponse, dependencies=[Depends(get_api_key)])
async def get_claim(
    claim_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
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

@router.post("/{claim_id}/photos", response_model=ClaimPhotoResponse, dependencies=[Depends(get_api_key)])
async def upload_claim_photo(
    claim_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Upload a photo for a claim.
    """
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
        photo_url=file_path, # Storing local path as URL for now
        photo_type=file.content_type
    )
    
    db.add(new_photo)
    await db.commit()
    await db.refresh(new_photo)
    
    return new_photo
