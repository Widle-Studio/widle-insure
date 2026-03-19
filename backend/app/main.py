from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import claims, policies
from app.core.config import settings
from app.core.log_config import setup_logging

import logging
# Configure logging on startup
setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS based on environment settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept", "x-api-key"],
)

from fastapi import Request
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time


    logger.info(
        f"{request.method} {request.url.path} "
        f"- {response.status_code} - {process_time:.2f}s"
    )


    return response

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_db

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    # Check database connection
    try:
        from sqlalchemy import text
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"


    return {
        "status": "healthy",
        "service": "widle-insure-backend",
        "database": db_status,
        "version": "0.1.0"
    }

@app.get("/")
async def root():
    """Root endpoint providing a welcome message."""
    return {"message": "Welcome to Widle Insure API"}

from app.api.v1.endpoints import claims, policies
from app.api.v1.endpoints.admin import auth as admin_auth
from app.api.v1.endpoints.admin import claims as admin_claims

app.include_router(claims.router, prefix=f"{settings.API_V1_STR}/claims", tags=["claims"])
app.include_router(policies.router, prefix=f"{settings.API_V1_STR}/policies", tags=["policies"])

app.include_router(admin_auth.router, prefix=f"{settings.API_V1_STR}/admin/auth", tags=["admin-auth"])
app.include_router(admin_claims.router, prefix=f"{settings.API_V1_STR}/admin/claims", tags=["admin-claims"])
