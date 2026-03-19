from anthropic import Anthropic
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class ClaudeAIService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY) if getattr(settings, 'ANTHROPIC_API_KEY', None) else None

    async def assess_damage(
        self,
        photo_urls: list[str],
        vehicle_info: dict,
        incident_info: dict
    ) -> dict:
        """
        Analyze damage photos using Claude Vision API

        Returns:
            {
                "severity": "minor" | "moderate" | "major" | "total_loss",
                "damaged_parts": ["front_bumper", "hood", ...],
                "estimated_cost": 2500.00,
                "confidence": 0.92,
                "fraud_indicators": [],
                "reasoning": "Analysis text..."
            }
        """
        prompt = self._build_damage_assessment_prompt(
            vehicle_info,
            incident_info
        )

        # TODO: Implement Claude API call with vision
        # For now, return mock data
        return {
            "severity": "moderate",
            "damaged_parts": ["front_bumper", "hood"],
            "estimated_cost": 2500.00,
            "confidence": 0.85,
            "fraud_indicators": [],
            "reasoning": "Mock analysis - implement Claude API"
        }

    def _build_damage_assessment_prompt(self, vehicle_info, incident_info):
        return f"""You are an auto insurance claims adjuster. Analyze this vehicle damage.

Vehicle: {vehicle_info['make']} {vehicle_info['model']} {vehicle_info['year']}
Incident: {incident_info['description']}
Date: {incident_info['date']}

Analyze the damage photos and provide:
1. Severity (minor/moderate/major/total_loss)
2. Damaged parts (specific components)
3. Estimated repair cost ($500-$15,000 range)
4. Fraud indicators (if any)
5. Confidence level (0-1)
6. Reasoning

Be conservative in estimates. If unclear, flag for human review."""

# Initialize service
ai_service = ClaudeAIService()
