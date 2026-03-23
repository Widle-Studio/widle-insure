from typing import Any, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import desc

from app.core.database import get_db
from app.core.security import get_api_key
from app.models.claims import Claim
from app.schemas.claims import ClaimResponse
from app.schemas.admin import ClaimStatusUpdate, ClaimActionResponse

router = APIRouter()

@router.get("/claims", response_model=List[ClaimResponse], dependencies=[Depends(get_api_key)])
async def list_all_claims(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filter claims by status"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    List all claims (paginated). Admin endpoint.
    """
    stmt = select(Claim).options(selectinload(Claim.photos)).order_by(desc(Claim.created_at))

    if status:
        stmt = stmt.where(Claim.status == status)

    stmt = stmt.offset(skip).limit(limit)

    result = await db.execute(stmt)
    claims = result.scalars().all()

    return claims

@router.get("/claims/{claim_id}", response_model=ClaimResponse, dependencies=[Depends(get_api_key)])
async def get_admin_claim(claim_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    """
    Get claim details for an admin.
    """
    stmt = select(Claim).where(Claim.id == claim_id).options(selectinload(Claim.photos))
    result = await db.execute(stmt)
    claim = result.scalars().first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    return claim

@router.patch("/claims/{claim_id}/status", response_model=ClaimActionResponse, dependencies=[Depends(get_api_key)])
async def update_claim_status(
    claim_id: uuid.UUID,
    status_update: ClaimStatusUpdate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Update the status of a claim directly.
    """
    stmt = select(Claim).where(Claim.id == claim_id)
    result = await db.execute(stmt)
    claim = result.scalars().first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    claim.status = status_update.status

    # Ideally: Add an audit log here logging `status_update.notes`

    await db.commit()
    await db.refresh(claim)

    return ClaimActionResponse(
        message="Claim status updated successfully",
        claim_id=str(claim.id),
        status=claim.status
    )

@router.post("/claims/{claim_id}/approve", response_model=ClaimActionResponse, dependencies=[Depends(get_api_key)])
async def approve_claim(claim_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    """
    Approve a claim.
    """
    stmt = select(Claim).where(Claim.id == claim_id)
    result = await db.execute(stmt)
    claim = result.scalars().first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    if claim.status == "approved":
        raise HTTPException(status_code=400, detail="Claim is already approved")

    claim.status = "approved"

    # Needs to log audit activity as 'approved'

    await db.commit()
    await db.refresh(claim)

    return ClaimActionResponse(
        message="Claim approved successfully",
        claim_id=str(claim.id),
        status=claim.status
    )

@router.post("/claims/{claim_id}/reject", response_model=ClaimActionResponse, dependencies=[Depends(get_api_key)])
async def reject_claim(claim_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    """
    Reject a claim.
    """
    stmt = select(Claim).where(Claim.id == claim_id)
    result = await db.execute(stmt)
    claim = result.scalars().first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    if claim.status == "rejected":
        raise HTTPException(status_code=400, detail="Claim is already rejected")

    claim.status = "rejected"

    # Needs to log audit activity as 'rejected'

    await db.commit()
    await db.refresh(claim)

    return ClaimActionResponse(
        message="Claim rejected successfully",
        claim_id=str(claim.id),
        status=claim.status
    )
