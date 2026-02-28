import logging

logger = logging.getLogger(__name__)

class AdjudicationService:
    """
    Service responsible for determining if a claim can be automatically approved,
    or if it requires human review. Implements strict, deterministic guardrails
    to prevent AI hallucination or probability errors from authorizing payouts.
    """

    # Deterministic Hard Limits
    MAX_AUTO_APPROVE_AMOUNT = 2000.00
    REQUIRED_AI_CONFIDENCE = 0.90
    MAX_FRAUD_SCORE = 10 # Assuming a scale of 0-100 where 0 is no risk

    @classmethod
    def evaluate_claim(cls, claim: dict, policy: dict, ai_analysis: dict, fraud_score: int) -> dict:
        """
        Evaluate a claim for auto-approval.

        Args:
            claim: Dictionary containing claim details (estimated_damage_cost, etc.)
            policy: Dictionary containing policy details (status, coverage_limit, deductible)
            ai_analysis: Dictionary containing AI results (confidence, red_flags)
            fraud_score: Integer representing risk score.

        Returns:
            dict: { "status": "Approved" | "Manual Review" | "Rejected", "reason": str }
        """
        reasons = []

        # 1. Deterministic Rule: Policy must be Active
        policy_status = policy.get("status")
        if not policy_status or policy_status.upper() != "ACTIVE":
            reasons.append("Policy is not active.")
            return {"status": "Rejected", "reason": " | ".join(reasons)}

        # Helper to safely parse floats
        def safe_float(val, default=0.0):
            try:
                return float(val) if val is not None else default
            except (TypeError, ValueError):
                return default

        estimated_cost = safe_float(claim.get("estimated_damage_cost"))

        # 2. Deterministic Rule: Hard Cap on Auto-Approval Amount
        if estimated_cost > cls.MAX_AUTO_APPROVE_AMOUNT:
            reasons.append(f"Estimated cost (${estimated_cost}) exceeds auto-approval limit (${cls.MAX_AUTO_APPROVE_AMOUNT}).")

        # 3. Deterministic Rule: Fraud Flags
        safe_fraud_score = safe_float(fraud_score)
        if safe_fraud_score > cls.MAX_FRAUD_SCORE:
            reasons.append(f"Fraud score ({safe_fraud_score}) exceeds acceptable limit ({cls.MAX_FRAUD_SCORE}).")

        # 4. Deterministic Rule: AI Red Flags
        # Even if AI confidence is high, explicit red flags must trigger review
        red_flags = ai_analysis.get("red_flags")
        if red_flags:
            reasons.append(f"AI identified red flags: {', '.join(red_flags)}.")

        # 5. Probabilistic Guardrail: AI Confidence Floor
        ai_confidence = safe_float(ai_analysis.get("confidence"))
        if ai_confidence < cls.REQUIRED_AI_CONFIDENCE:
            reasons.append(f"AI confidence ({ai_confidence}) is below required threshold ({cls.REQUIRED_AI_CONFIDENCE}).")

        # 6. Deterministic Rule: Coverage Limits
        coverage_limit = safe_float(policy.get("coverage_limit"))
        deductible = safe_float(policy.get("deductible"))

        if estimated_cost > (coverage_limit - deductible):
             reasons.append(f"Estimated cost (${estimated_cost}) exceeds coverage limit minus deductible (${coverage_limit - deductible}).")

        # Decision Logic
        if reasons:
            return {"status": "Manual Review", "reason": " | ".join(reasons)}

        # If all deterministic guardrails pass, approve.
        return {"status": "Approved", "reason": "Passed all auto-adjudication guardrails."}

adjudication_service = AdjudicationService()
