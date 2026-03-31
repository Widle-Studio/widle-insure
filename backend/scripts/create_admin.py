"""Create initial admin user from environment variables"""
import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import AsyncSessionLocal
from app.models.users import User
from app.core.security import get_password_hash

async def create_admin():
    """Create admin user if doesn't exist"""
    email = os.getenv("FIRST_ADMIN_EMAIL", "admin@widle.com")
    password = os.getenv("FIRST_ADMIN_PASSWORD", "changeme123")

    async with AsyncSessionLocal() as db:
        # Check if admin exists
        result = await db.execute(select(User).filter(User.email == email))
        existing = result.scalar_one_or_none()

        if existing:
            print(f"✓ Admin user {email} already exists")
            return

        # Create admin user
        admin = User(
            email=email,
            hashed_password=get_password_hash(password),
            is_admin=True
        )
        db.add(admin)
        await db.commit()
        print(f"✅ Created admin user: {email}")

if __name__ == "__main__":
    asyncio.run(create_admin())
