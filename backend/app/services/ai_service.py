import base64
import json
import logging
import os
import re

import aiofiles
from anthropic import AsyncAnthropic

from app.core.config import settings

logger = logging.getLogger(__name__)


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent prompt injection."""
    return re.sub(r'<[^>]*>', '', str(text))


class ClaudeAIService:
    def __init__(self):
        # We need to handle async call, so AsyncAnthropic
        self.client = AsyncAnthropic(api_key=getattr(settings, 'ANTHROPIC_API_KEY', '')) if getattr(settings, 'ANTHROPIC_API_KEY', None) else None

    async def _encode_image(self, photo_path: str) -> dict | None:
        """Read a local image file and encode it as base64 for Anthropic API."""
        try:
            # photo_urls are typically local paths (e.g., /static/uploads/...) based on current implementation
            # We strip the leading slash if present to make it a relative path to the current working directory
            local_path = photo_path.lstrip("/")

            if not os.path.exists(local_path):
                logger.warning(f"Image not found at path: {local_path}")
                return None

            async with aiofiles.open(local_path, "rb") as image_file:
                image_data = await image_file.read()
                base64_image = base64.b64encode(image_data).decode("utf-8")

            _, ext = os.path.splitext(local_path)
            media_type = f"image/{ext.lower().replace('.', '')}"
            if media_type == "image/jpg":
                media_type = "image/jpeg"

            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64_image,
                },
            }
        except Exception as e:
            logger.error(f"Error encoding image {photo_path}: {e}")
            return None

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
        if not self.client:
            logger.warning("Anthropic API key not configured. Returning mock data.")
            return {
                "severity": "moderate",
                "damaged_parts": ["front_bumper", "hood"],
                "estimated_cost": 2500.00,
                "confidence": 0.85,
                "fraud_indicators": [],
                "reasoning": "Mock analysis - implement Claude API"
            }

        # Build content block for the message
        content = []

        # Process each image
        for url in photo_urls:
            # Assume it's a local file for now based on current app implementation
            image_block = await self._encode_image(url)
            if image_block:
                content.append(image_block)

        # Add the text prompt
        text_prompt = self._build_damage_assessment_prompt(vehicle_info, incident_info)
        content.append({
            "type": "text",
            "text": text_prompt
        })

        system_prompt = """You are an auto insurance claims adjuster. Analyze the vehicle damage photo provided.
Provide your analysis based on the photo and the provided context.
You must return the result EXACTLY as a valid JSON object matching this schema:
{
    "severity": "minor" | "moderate" | "major" | "total_loss",
    "damaged_parts": ["list", "of", "parts"],
    "estimated_cost": 2500.00,
    "confidence": 0.95,
    "fraud_indicators": ["any", "red", "flags"],
    "reasoning": "Detailed explanation of your analysis..."
}
Do not include any other text before or after the JSON."""

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": content,
                    }
                ]
            )

            # Parse the JSON response
            response_text = response.content[0].text
            # Attempt to extract JSON if Claude added conversational wrapper
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()

            result = json.loads(json_str)
            return result

        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            # Fallback mock data in case of error
            return {
                "severity": "moderate",
                "damaged_parts": ["front_bumper", "hood"],
                "estimated_cost": 2500.00,
                "confidence": 0.85,
                "fraud_indicators": [],
                "reasoning": f"Error occurred during analysis: {str(e)}"
            }

    def _build_damage_assessment_prompt(self, vehicle_info, incident_info):
        return f"""Here is the context for the claim:
<vehicle_context>
<make>{sanitize_input(vehicle_info.get('make', ''))}</make>
<model>{sanitize_input(vehicle_info.get('model', ''))}</model>
<year>{sanitize_input(vehicle_info.get('year', ''))}</year>
</vehicle_context>
<incident_context>
<date>{sanitize_input(incident_info.get('date', ''))}</date>
<description>{sanitize_input(incident_info.get('description', ''))}</description>
</incident_context>

Be conservative in your estimates. If unsure, flag for human review.
"""

# Initialize service
ai_service = ClaudeAIService()
