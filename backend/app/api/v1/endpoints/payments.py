import uuid
from typing import Any
import datetime
import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import get_api_key
from app.models.claims import Claim
from app.schemas.claims import ClaimResponse

router = APIRouter()

@router.post("/{claim_id}/payout", response_model=ClaimResponse, dependencies=[Depends(get_api_key)])
async def initiate_payout(claim_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    """
    Initiate payout for a claim.
    """
    result = await db.execute(select(Claim).where(Claim.id == claim_id))
    claim = result.scalars().first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    if claim.status != "Approved":
        raise HTTPException(status_code=400, detail="Only approved claims can be paid out")

    # Mock Stripe transfer
    transfer_id = f"tr_{secrets.token_hex(12)}"

    claim.status = "Paid"
    # Note: adding basic audit log / fields would be ideal here if they existed
    # like payout_id, payout_status, payout_date, but for now we just change status

    await db.commit()
    await db.refresh(claim)

    return claim
