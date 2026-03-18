import uuid
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.models.claims import Claim
from app.schemas.claims import ClaimResponse

router = APIRouter()


@router.get("/", response_model=List[ClaimResponse])
async def list_claims(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin_user),
) -> Any:
    """
    List all claims (admin).
    """
    query = select(Claim).options(selectinload(Claim.photos))
    if status:
        query = query.where(Claim.status == status)

    query = query.offset(skip).limit(limit).order_by(Claim.created_at.desc())
    result = await db.execute(query)
    claims = result.scalars().all()
    return claims


@router.get("/{claim_id}", response_model=ClaimResponse)
async def get_claim(
    claim_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin_user),
) -> Any:
    """
    Get claim details (admin).
    """
    result = await db.execute(
        select(Claim)
        .where(Claim.id == claim_id)
        .options(selectinload(Claim.photos))
    )
    claim = result.scalars().first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim


@router.patch("/{claim_id}/status", response_model=ClaimResponse)
async def update_claim_status(
    claim_id: uuid.UUID,
    status: str,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin_user),
) -> Any:
    """
    Update claim status.
    """
    result = await db.execute(
        select(Claim)
        .where(Claim.id == claim_id)
        .options(selectinload(Claim.photos))
    )
    claim = result.scalars().first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    claim.status = status
    await db.commit()
    await db.refresh(claim)
    return claim


@router.post("/{claim_id}/approve", response_model=ClaimResponse)
async def approve_claim(
    claim_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin_user),
) -> Any:
    """
    Approve a claim.
    """
    result = await db.execute(
        select(Claim)
        .where(Claim.id == claim_id)
        .options(selectinload(Claim.photos))
    )
    claim = result.scalars().first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    claim.status = "Approved"
    await db.commit()
    await db.refresh(claim)
    return claim


@router.post("/{claim_id}/reject", response_model=ClaimResponse)
async def reject_claim(
    claim_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin_user),
) -> Any:
    """
    Reject a claim.
    """
    result = await db.execute(
        select(Claim)
        .where(Claim.id == claim_id)
        .options(selectinload(Claim.photos))
    )
    claim = result.scalars().first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    claim.status = "Rejected"
    await db.commit()
    await db.refresh(claim)
    return claim


@router.get("/metrics/analytics")
async def get_analytics(
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin_user),
) -> Any:
    """
    Get analytics for admin dashboard.
    """
    total_claims_result = await db.execute(select(func.count(Claim.id)))
    total_claims = total_claims_result.scalar()

    approved_claims_result = await db.execute(
        select(func.count(Claim.id)).where(Claim.status == "Approved")
    )
    approved_claims = approved_claims_result.scalar()

    pending_claims_result = await db.execute(
        select(func.count(Claim.id)).where(Claim.status == "New")
    )
    pending_claims = pending_claims_result.scalar()

    rejected_claims_result = await db.execute(
        select(func.count(Claim.id)).where(Claim.status == "Rejected")
    )
    rejected_claims = rejected_claims_result.scalar()

    stp_rate = 0.0
    if total_claims and total_claims > 0:
        stp_rate = round((approved_claims / total_claims) * 100, 2)

    return {
        "total_claims": total_claims or 0,
        "approved_claims": approved_claims or 0,
        "pending_claims": pending_claims or 0,
        "rejected_claims": rejected_claims or 0,
        "stp_rate": stp_rate,
    }
