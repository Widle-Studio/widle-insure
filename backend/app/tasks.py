import asyncio
import logging
from typing import Dict, Any

from app.core.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.claims import Claim
from app.services.ai_service import ai_service
from app.services.adjudication_service import adjudication_service
from app.services.email import email_service
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)

async def process_claim_analysis_async(claim_id: str):
    async with AsyncSessionLocal() as db:
        stmt = select(Claim).where(Claim.id == claim_id).options(selectinload(Claim.photos))
        result = await db.execute(stmt)
        claim_with_photos = result.scalars().first()

        if not claim_with_photos or not claim_with_photos.photos:
            logger.error(f"Claim {claim_id} not found or has no photos")
            return

        photo_urls = [photo.photo_url for photo in claim_with_photos.photos]

        # Call AI service
        analysis = await ai_service.assess_damage(
            photo_urls=photo_urls,
            vehicle_info={
                "make": claim_with_photos.vehicle_make,
                "model": claim_with_photos.vehicle_model,
                "year": claim_with_photos.vehicle_year,
            },
            incident_info={
                "description": claim_with_photos.incident_description,
                "date": str(claim_with_photos.incident_date) if claim_with_photos.incident_date else "",
            }
        )

        claim_with_photos.estimated_damage_cost = analysis.get("estimated_cost")

        # Store AI analysis in photos
        for photo in claim_with_photos.photos:
            photo.ai_analysis = analysis

        # Mock Policy and Fraud Score
        mock_policy = {
            "status": "Active",
            "coverage_limit": 50000.0,
            "deductible": 500.0
        }

        mock_fraud_score = 0
        if claim_with_photos.estimated_damage_cost and float(claim_with_photos.estimated_damage_cost) > 10000:
            mock_fraud_score += 15

        # Trigger Auto-Adjudication
        claim_dict = {"estimated_damage_cost": claim_with_photos.estimated_damage_cost}
        adjudication_result = adjudication_service.evaluate_claim(
            claim=claim_dict,
            policy=mock_policy,
            ai_analysis=analysis,
            fraud_score=mock_fraud_score
        )

        new_status = adjudication_result["status"]
        claim_with_photos.status = new_status

        if new_status == "Approved":
            claim_with_photos.approved_amount = claim_with_photos.estimated_damage_cost
            email_body = f"Your claim {claim_with_photos.claim_number} has been automatically approved for ${claim_with_photos.approved_amount}!"
            await email_service.send_email(
                to=claim_with_photos.claimant_email,
                subject="Claim Approved",
                body=email_body
            )
        elif new_status == "Manual Review":
            email_body = f"Your claim {claim_with_photos.claim_number} is currently under manual review."
            await email_service.send_email(
                to=claim_with_photos.claimant_email,
                subject="Claim Under Review",
                body=email_body
            )

        await db.commit()

@celery_app.task(name="app.tasks.ai_analysis_task")
def analyze_claim_task(claim_id: str):
    """Background task to analyze a claim using AI and auto-adjudicate."""
    asyncio.run(process_claim_analysis_async(claim_id))
    return {"status": "Analysis completed", "claim_id": claim_id}
