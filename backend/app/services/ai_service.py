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

        if self.client:
            try:
                # In a real implementation we would download the image bytes and pass them to Claude.
                # For this Alpha sprint, if the client is configured, we'll simulate a basic response based on the prompt
                response = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1000,
                    system="You are an expert auto insurance claims adjuster.",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                # In a real scenario, we'd parse the structured output from the LLM response.
                # Here we'll fallback to the mock for predictable UI rendering during alpha.
            except Exception as e:
                logger.error(f"Claude API failed: {e}")

        # Default fallback for predictable Alpha sprint testing
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
