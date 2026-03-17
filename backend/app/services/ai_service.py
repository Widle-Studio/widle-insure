import re
import json
import httpx
import base64
from typing import Dict, Any, Optional
from anthropic import AsyncAnthropic

from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent prompt injection."""
    if not text:
        return ""
    # Remove any XML-like tags that could interfere with the prompt structure
    return re.sub(r'<[^>]*>', '', str(text))

class AIService:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None

    async def _fetch_image_as_base64(self, photo_url: str) -> Optional[str]:
        # For a local URL, we might need to read it from disk if it starts with / or uploads/
        # But if it's external, we fetch it.
        import os
        import aiofiles

        try:
            if photo_url.startswith("http://") or photo_url.startswith("https://"):
                async with httpx.AsyncClient() as client:
                    response = await client.get(photo_url)
                    response.raise_for_status()
                    return base64.b64encode(response.content).decode("utf-8")
            else:
                # Local file handling - Secure against LFI
                base_dir = os.path.abspath("uploads")
                target_path = os.path.abspath(photo_url)

                # Check if the target path is within the allowed uploads directory
                if not target_path.startswith(base_dir):
                    logger.warning(f"Security: Attempt to read file outside of uploads directory: {photo_url}")
                    return None

                if not os.path.exists(target_path):
                    logger.warning(f"File not found: {target_path}")
                    return None

                async with aiofiles.open(target_path, "rb") as f:
                    content = await f.read()
                    return base64.b64encode(content).decode("utf-8")
        except Exception as e:
            logger.error(f"Error fetching image for AI analysis from {photo_url}: {e}")
            return None

    def _determine_mime_type(self, photo_url: str) -> str:
        url_lower = photo_url.lower()
        if url_lower.endswith('.png'):
            return 'image/png'
        if url_lower.endswith('.webp'):
            return 'image/webp'
        return 'image/jpeg' # Default to jpeg

    async def analyze_damage(self, photo_url: str, vehicle_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze vehicle damage using Claude Vision API.
        Returns a dictionary with damage severity, damaged parts, estimated cost, red flags, and confidence.
        """
        if not self.client:
            logger.warning("ANTHROPIC_API_KEY is not set. Using rule-based fallback for damage estimation.")
            return self._rule_based_fallback()

        image_data = await self._fetch_image_as_base64(photo_url)
        if not image_data:
            logger.warning(f"Could not load image {photo_url}. Using rule-based fallback.")
            return self._rule_based_fallback()

        mime_type = self._determine_mime_type(photo_url)

        system_prompt = """You are an auto insurance claims adjuster. Analyze the vehicle damage photo provided.
Provide your analysis based on the photo and the provided context.
Strictly follow the output format provided.
Output ONLY valid JSON matching this schema:
{
  "damage_severity": "Minor|Moderate|Major|Total Loss",
  "damaged_parts": ["part1", "part2"],
  "estimated_repair_cost": "dollar amount range",
  "red_flags": ["flag1", "flag2"] or [],
  "confidence": "High|Medium|Low"
}"""

        user_content = f"""Here is the context for the claim:
<vehicle_context>
<make>{sanitize_input(vehicle_context.get('make', ''))}</make>
<model>{sanitize_input(vehicle_context.get('model', ''))}</model>
<year>{sanitize_input(vehicle_context.get('year', ''))}</year>
</vehicle_context>
<incident_context>
<date>{sanitize_input(vehicle_context.get('incident_date', ''))}</date>
<location>{sanitize_input(vehicle_context.get('incident_location', ''))}</location>
</incident_context>

Provide your analysis in the requested JSON format.
"""

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": mime_type,
                                    "data": image_data
                                }
                            },
                            {
                                "type": "text",
                                "text": user_content
                            }
                        ]
                    }
                ]
            )

            # Parse the JSON response
            response_text = response.content[0].text
            # Basic cleanup in case Claude adds markdown code blocks
            clean_json = re.sub(r'```json\n|\n```', '', response_text).strip()

            return json.loads(clean_json)

        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            return self._rule_based_fallback()

    def _rule_based_fallback(self) -> Dict[str, Any]:
        """Provides a basic fallback if AI analysis fails or is not configured."""
        return {
            "damage_severity": "Moderate",
            "damaged_parts": ["Unknown (AI analysis failed)"],
            "estimated_repair_cost": "$2000-5000",
            "red_flags": [],
            "confidence": "Low"
        }

ai_service = AIService()
