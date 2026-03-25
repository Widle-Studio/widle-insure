import asyncio
import os
import random
import uuid
from datetime import datetime, timedelta
import argparse

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.models.claims import Claim, ClaimPhoto
from app.models.users import AdminUser
from app.core.security import get_password_hash

# Generate some realistic-looking dummy data
first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
makes_models = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Highlander", "Tacoma"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Odyssey"],
    "Ford": ["F-150", "Escape", "Explorer", "Mustang", "Focus"],
    "Chevrolet": ["Silverado", "Equinox", "Malibu", "Tahoe", "Colorado"],
    "Nissan": ["Altima", "Sentra", "Rogue", "Pathfinder", "Maxima"],
    "Tesla": ["Model 3", "Model Y", "Model S", "Model X"]
}
locations = [
    "123 Main St, Springfield, IL", "456 Oak Ave, Austin, TX", "789 Pine Ln, Denver, CO", "101 Elm Blvd, Seattle, WA",
    "202 Maple Dr, Miami, FL", "303 Cedar Ct, Boston, MA", "404 Walnut Way, Atlanta, GA", "505 Birch St, Phoenix, AZ",
    "606 Ash Ave, Chicago, IL", "707 Cherry Ln, Dallas, TX", "808 Poplar Blvd, San Diego, CA", "909 Spruce Dr, Portland, OR",
    "Intersection of 5th and Broadway, New York, NY", "I-95 Northbound near Exit 45", "Parking lot at 1000 Commercial Pkwy"
]
descriptions = [
    "Rear-ended at a stoplight by a distracted driver.", "Backed into a pole in a parking garage.",
    "Swiped on the passenger side while parked on the street overnight.", "Hit a deer on a rural highway.",
    "T-boned at an intersection by a car running a red light.", "Hail damage from severe thunderstorm.",
    "Windshield cracked by a rock kicked up by a truck.", "Vandalism: key scratch along the driver's side.",
    "Sideswiped by another vehicle merging onto the freeway.", "Front bumper damaged from hitting a high curb."
]

async def create_demo_data(num_claims=50):
    """Seeds the database with realistic test claims for Demo & Performance testing."""
    print(f"Connecting to database: {settings.SQLALCHEMY_DATABASE_URI}")
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        try:
            # 1. Ensure an admin user exists
            from sqlalchemy.future import select
            result = await db.execute(select(AdminUser).where(AdminUser.email == "admin@widle.com"))
            admin = result.scalars().first()
            if not admin:
                print("Creating default admin user (admin@widle.com / admin123)...")
                new_admin = AdminUser(
                    email="admin@widle.com",
                    hashed_password=get_password_hash("admin123"),
                    full_name="System Admin",
                    is_active=True,
                    is_superuser=True
                )
                db.add(new_admin)
                await db.commit()

            # 2. Generate N claims
            print(f"Generating {num_claims} demo claims...")
            claims_created = 0

            for i in range(num_claims):
                # Randomize claim details
                make = random.choice(list(makes_models.keys()))
                model = random.choice(makes_models[make])
                year = random.randint(2010, 2024)

                # Determine claim type/status for variety
                # Mix: 40% Approved (Auto), 40% Pending (Human Review), 10% Rejected, 10% Paid
                status_roll = random.random()
                if status_roll < 0.4:
                    status = "Approved"
                    damage_cost = round(random.uniform(500, 1900), 2) # Auto-approvals usually < $2000
                elif status_roll < 0.8:
                    status = "New" # Needs review
                    # High damage or fraud flags push it to review
                    damage_cost = round(random.uniform(2500, 15000), 2)
                elif status_roll < 0.9:
                    status = "Rejected"
                    damage_cost = round(random.uniform(100, 5000), 2)
                else:
                    status = "Paid"
                    damage_cost = round(random.uniform(800, 4500), 2)

                # Generate date within last 90 days
                days_ago = random.randint(1, 90)
                incident_date = datetime.now() - timedelta(days=days_ago)
                created_at = incident_date + timedelta(days=random.randint(0, 3)) # Reported 0-3 days later

                # Fraud example: Reported > 30 days later
                if i % 10 == 0:
                    created_at = incident_date + timedelta(days=45)
                    status = "New" # Force manual review due to delay

                claim = Claim(
                    policy_number=f"POL-{random.randint(100000000, 999999999)}",
                    claim_number=f"CLM-{created_at.year}-{str(random.randint(1, 999999)).zfill(6)}",
                    claimant_name=f"{random.choice(first_names)} {random.choice(last_names)}",
                    claimant_phone=f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                    claimant_email=f"claimant{i}@example.com",
                    incident_date=incident_date,
                    incident_location=random.choice(locations),
                    incident_description=random.choice(descriptions),
                    vehicle_vin=f"1HGCM82633A{random.randint(100000, 999999)}",
                    vehicle_make=make,
                    vehicle_model=model,
                    vehicle_year=year,
                    status=status,
                    estimated_damage_cost=damage_cost,
                    approved_amount=damage_cost if status in ["Approved", "Paid"] else None,
                    created_at=created_at,
                    updated_at=created_at + timedelta(hours=random.randint(1, 48))
                )
                db.add(claim)
                await db.flush() # Get claim ID

                # Add a mock photo with AI analysis
                ai_analysis = {
                    "severity": "minor" if damage_cost < 2000 else "major",
                    "confidence": random.uniform(0.7, 0.99),
                    "damaged_parts": ["front_bumper", "headlight"] if "front" in claim.incident_description.lower() else ["rear_bumper"],
                    "red_flags": ["Delayed reporting"] if (created_at - incident_date).days > 30 else []
                }

                photo = ClaimPhoto(
                    claim_id=claim.id,
                    photo_url=f"/static/demo/damage_{random.randint(1,5)}.jpg",
                    photo_type="damage",
                    ai_analysis=ai_analysis
                )
                db.add(photo)
                claims_created += 1

            await db.commit()
            print(f"Successfully seeded {claims_created} demo claims.")

        except Exception as e:
            await db.rollback()
            print(f"Error seeding data: {e}")
            raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed demo data for Widle Insure")
    parser.add_argument("--count", type=int, default=50, help="Number of claims to generate (e.g., 100 for performance testing)")
    args = parser.parse_args()

    asyncio.run(create_demo_data(num_claims=args.count))
