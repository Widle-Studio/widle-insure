from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import get_db

router = APIRouter()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Enhanced health check with database status"""

    # Check database connection
    db_status = "unknown"
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    # Check if migrations are current (optional)
    migration_status = "unknown"
    try:
        result = await db.execute(text("SELECT version_num FROM alembic_version"))
        version = result.scalar_one_or_none()
        migration_status = version if version else "no migrations"
    except:
        migration_status = "not initialized"

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "service": "widle-insure-api",
        "database": db_status,
        "migrations": migration_status
    }
