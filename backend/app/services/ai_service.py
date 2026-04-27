import asyncio
import base64
import json
import logging
import os
import re

import aiofiles
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from app.core.config import settings
from app.services.vision_service import yolo_vision_service

logger = logging.getLogger(__name__)


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent prompt injection."""
    return re.sub(r"<[^>]*>", "", str(text))


class ClaudeAIService:
    def __init__(self):
        api_key = getattr(settings, "ANTHROPIC_API_KEY", None)
        self.client = (
            ChatAnthropic(
                model_name="claude-3-5-sonnet-20241022",
                anthropic_api_key=api_key,
                max_tokens=1024,
            )
            if api_key
            else None
        )

    async def _encode_image(self, photo_path: str) -> dict | None:
        """Read a local image file and encode it as base64 for Anthropic API."""
        try:
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
                "type": "image_url",
                "image_url": {"url": f"data:{media_type};base64,{base64_image}"},
            }
        except Exception as e:
            logger.error(f"Error encoding image {photo_path}: {e}")
            return None

    async def assess_damage(
        self, photo_urls: list[str], vehicle_info: dict, incident_info: dict
    ) -> dict:
        if not self.client:
            logger.warning("Anthropic API key not configured. Returning mock data.")
            return {
                "severity": "moderate",
                "damaged_parts": ["front_bumper", "hood"],
                "estimated_cost": 2500.00,
                "confidence": 0.85,
                "fraud_indicators": [],
                "reasoning": "Mock analysis - implement Claude API",
            }

        # Concurrently encode images and run YOLO inference
        encode_tasks = [self._encode_image(url) for url in photo_urls]
        image_blocks, vision_result = await asyncio.gather(
            asyncio.gather(*encode_tasks),
            asyncio.to_thread(yolo_vision_service.detect_damage, photo_urls),
        )

        content = []
        for image_block in image_blocks:
            if image_block:
                content.append(image_block)

        text_prompt = self._build_damage_assessment_prompt(
            vehicle_info, incident_info, vision_result
        )
        content.append({"type": "text", "text": text_prompt})

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
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=content),
            ]
            response = await self.client.ainvoke(messages)

            response_text = response.content
            if isinstance(response_text, list):
                response_text = response_text[0].get("text", "")

            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()

            result = json.loads(json_str)
            return result

        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            return {
                "severity": "moderate",
                "damaged_parts": ["front_bumper", "hood"],
                "estimated_cost": 2500.00,
                "confidence": 0.85,
                "fraud_indicators": [],
                "reasoning": f"Error occurred during analysis: {str(e)}",
            }

    def _build_damage_assessment_prompt(
        self, vehicle_info, incident_info, vision_result
    ):
        vision_context = ""
        if vision_result.get("status") == "success" and vision_result.get("detections"):
            vision_context = f"""
<computer_vision_analysis>
The initial automated computer vision system (YOLOv8) detected the following:
- Highest Severity Detected: {sanitize_input(vision_result.get("highest_severity", "unknown"))}
- Damaged Parts Detected: {", ".join([sanitize_input(p) for p in vision_result.get("damaged_parts", [])])}
</computer_vision_analysis>
Use this computer vision data to inform your cost estimation and final adjudication, but ultimately rely on your own visual assessment of the photos provided.
"""

        return f"""Here is the context for the claim:
<vehicle_context>
<make>{sanitize_input(vehicle_info.get("make", ""))}</make>
<model>{sanitize_input(vehicle_info.get("model", ""))}</model>
<year>{sanitize_input(vehicle_info.get("year", ""))}</year>
</vehicle_context>
<incident_context>
<date>{sanitize_input(incident_info.get("date", ""))}</date>
<description>{sanitize_input(incident_info.get("description", ""))}</description>
</incident_context>
{vision_context}
Be conservative in your estimates. If unsure, flag for human review.
"""


ai_service = ClaudeAIService()
