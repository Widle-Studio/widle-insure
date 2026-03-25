import logging
import secrets
import uuid
from typing import Any

import stripe
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_api_key
from app.models.claims import Claim
from app.schemas.claims import ClaimResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Configure Stripe API Key
stripe.api_key = settings.STRIPE_SECRET_KEY

@router.post("/{claim_id}/payout", response_model=ClaimResponse, dependencies=[Depends(get_api_key)])
async def initiate_payout(claim_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    """
    Initiate Stripe ACH/transfer payout for a claim.
    """
    result = await db.execute(select(Claim).where(Claim.id == claim_id))
    claim = result.scalars().first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    if claim.status != "Approved":
        raise HTTPException(status_code=400, detail="Only approved claims can be paid out")

    # The actual Stripe integration
    try:
        # For an alpha MVP, if the Stripe Secret Key isn't provided, use a mock transfer ID.
        if settings.STRIPE_SECRET_KEY:
            # We assume a dummy destination account since we don't capture this strictly in the FNOL form yet.
            # In a production app, the claimant would link their bank account via Stripe Connect.
            mock_destination = "acct_1032D82eZvKYlo2C"

            # Amount is expected in cents
            amount_in_cents = int(claim.approved_amount * 100) if claim.approved_amount else 0

            if amount_in_cents > 0:
                # Synchronous Stripe API calls. Depending on load, might wrap in asyncio.to_thread()
                transfer = stripe.Transfer.create(
                    amount=amount_in_cents,
                    currency="usd",
                    destination=mock_destination,
                    description=f"Insurance claim payout: {claim.claim_number}"
                )
                transfer_id = transfer.id
            else:
                raise ValueError("Approved amount must be greater than zero.")
        else:
            logger.info("STRIPE_SECRET_KEY not set. Mocking Stripe payout transfer.")
            transfer_id = f"tr_{secrets.token_hex(12)}"

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error during payout for claim {claim_id}: {str(e)}")
        raise HTTPException(status_code=502, detail=f"Payment gateway error: {e.user_message}")
    except Exception as e:
        logger.error(f"Unexpected error during payout: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during payout")

    claim.status = "Paid"
    # Note: A real implementation would store transfer_id in a new column on the Claim model

    await db.commit()
    await db.refresh(claim)

    return claim
