import asyncio
import uuid
from datetime import datetime
from app.core.database import AsyncSessionLocal, engine
from app.models.claims import Claim
from sqlalchemy import select

async def seed_data():
    async with AsyncSessionLocal() as session:
        # Check if data exists
        result = await session.execute(select(Claim))
        if result.scalars().first():
            print("Data already exists. Skipping seed.")
            return

        print("Seeding test claims...")
        
        claims = [
            Claim(
                id=uuid.uuid4(),
                policy_number="POL-123456789",
                claim_number=f"CLM-2024-{i:03d}",
                claimant_name=f"User {i}",
                claimant_phone="555-0100",
                claimant_email=f"user{i}@example.com",
                incident_date=datetime.now(),
                incident_location="123 Main St",
                incident_description="Rear-end collision",
                vehicle_vin=f"VIN{i}123456789",
                vehicle_make="Toyota",
                vehicle_model="Camry",
                vehicle_year=2020,
                status="pending"
            ) for i in range(1, 11)
        ]
        
        session.add_all(claims)
        await session.commit()
        print(f"Successfully created {len(claims)} test claims.")

if __name__ == "__main__":
    asyncio.run(seed_data())
