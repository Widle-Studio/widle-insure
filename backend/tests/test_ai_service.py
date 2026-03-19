import pytest
from app.services.ai_service import ClaudeAIService

@pytest.mark.asyncio
async def test_assess_damage():
    ai_service = ClaudeAIService()

    analysis = await ai_service.assess_damage(
        photo_urls=["http://example.com/photo.jpg"],
        vehicle_info={"make": "Toyota", "model": "Camry", "year": 2020},
        incident_info={"description": "Rear-end collision", "date": "2024-03-01"}
    )

    assert analysis["severity"] == "moderate"
    assert "front_bumper" in analysis["damaged_parts"]
    assert analysis["estimated_cost"] == 2500.00
    assert analysis["confidence"] == 0.85
