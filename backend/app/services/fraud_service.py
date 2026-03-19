import logging
from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.claims import Claim

logger = logging.getLogger(__name__)

class FraudDetectionService:
    """
    Service responsible for calculating fraud risk scores based on deterministic rules
    and historical claim data analysis.
    """

    async def calculate_fraud_score(self, claim: Claim, db: AsyncSession, ai_confidence: float = 1.0) -> int:
        """
        Calculate a fraud score (0-100) based on predefined rules.
        """
        score = 0

        # Rule 1: Time delay
        # Claim submitted >30 days after incident
        if claim.incident_date:
            # Ensure we compare timezone-aware or naive datetimes correctly
            now = datetime.now(timezone.utc)
            if claim.incident_date.tzinfo is None:
                incident_date = claim.incident_date.replace(tzinfo=timezone.utc)
            else:
                incident_date = claim.incident_date

            days_delayed = (now - incident_date).days
            if days_delayed > 30:
                score += 20

        # Rule 2: Claim amount
        # Unusually high claim amount
        if claim.estimated_damage_cost and claim.estimated_damage_cost > 10000:
            score += 15

        # Rule 3: Recent claims
        # Multiple claims in short period (e.g., 90 days)
        if claim.policy_number:
            ninety_days_ago = datetime.now(timezone.utc).replace(day=1) # simplified for alpha
            # In a real app we'd do: datetime.now(timezone.utc) - timedelta(days=90)

            stmt = select(func.count(Claim.id)).where(
                Claim.policy_number == claim.policy_number,
                Claim.id != claim.id,
                # For alpha, we just check total previous claims for the policy
            )
            result = await db.execute(stmt)
            recent_claims = result.scalar() or 0
            if recent_claims >= 1:
                score += 25

        # Rule 4: AI confidence
        # Low confidence from the AI damage assessment
        if ai_confidence < 0.7:
            score += 15

        # Ensure score stays within 0-100 bounds
        return min(max(score, 0), 100)

fraud_service = FraudDetectionService()
