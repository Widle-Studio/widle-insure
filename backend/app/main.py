from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging

# Configure logging on startup
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "widle-insure-backend"}

@app.get("/")
async def root():
    return {"message": "Welcome to Widle Insure API"}

from app.api.v1.endpoints import claims, policies
app.include_router(claims.router, prefix=f"{settings.API_V1_STR}/claims", tags=["claims"])
app.include_router(policies.router, prefix=f"{settings.API_V1_STR}/policies", tags=["policies"])
