import asyncio
import uuid
from datetime import datetime

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.claims import Claim


import argparse
from app.models.claims import ClaimPhoto

async def seed_data(count: int, with_photos: bool):
    async with AsyncSessionLocal() as session:
        # Check if data exists
        result = await session.execute(select(Claim))
        if result.scalars().first():
            print("Data already exists. Skipping seed.")
            return

        print(f"Seeding {count} test claims...")
        
        claims = []
        for i in range(1, count + 1):
            claim_id = uuid.uuid4()
            claim = Claim(
                id=claim_id,
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
            )
            claims.append(claim)


            if with_photos:
                photo = ClaimPhoto(
                    id=uuid.uuid4(),
                    claim_id=claim_id,
                    photo_url=f"http://example.com/mock-photo-{i}.jpg",
                    photo_type="image/jpeg"
                )
                session.add(photo)

        session.add_all(claims)
        await session.commit()
        print(f"Successfully created {len(claims)} test claims.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed database with mock data.")
    parser.add_argument("--count", type=int, default=10, help="Number of claims to create")
    parser.add_argument("--with-photos", action="store_true", help="Include mock photos with claims")
    args = parser.parse_args()

    asyncio.run(seed_data(count=args.count, with_photos=args.with_photos))
