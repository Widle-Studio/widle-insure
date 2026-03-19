import logging
from datetime import datetime
from typing import Dict, Any

from app.models.claims import Claim

logger = logging.getLogger(__name__)

class FraudService:
    """
    Service responsible for calculating the fraud score of a claim based on predefined rules.
    """

    @classmethod
    def calculate_fraud_score(cls, claim: Claim, ai_analysis: Dict[str, Any], recent_claims_count: int = 0) -> int:
        """
        Calculate fraud score for a given claim.
        Scale of 0-100 where higher score means higher probability of fraud.
        """
        score = 0

        # Time delay
        created_at = claim.created_at or datetime.now()
        if claim.incident_date:
            try:
                days_delayed = (created_at.replace(tzinfo=None) - claim.incident_date.replace(tzinfo=None)).days
                if days_delayed > 30:
                    score += 20
            except Exception as e:
                logger.warning(f"Error calculating time delay: {e}")

        # Claim amount
        if claim.estimated_damage_cost and claim.estimated_damage_cost > 10000:
            score += 15

        # Recent claims
        if recent_claims_count > 1:
            score += 25

        # AI confidence
        ai_confidence = ai_analysis.get("confidence")
        if ai_confidence is not None and ai_confidence < 0.7:
            score += 15

        # Red flags from AI
        if ai_analysis.get("red_flags"):
            score += 20

        return min(max(score, 0), 100)

fraud_service = FraudService()
