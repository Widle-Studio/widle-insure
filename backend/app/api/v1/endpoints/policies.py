
import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import redis.asyncio as redis

from app.core.config import settings

from app.core.security import get_api_key

router = APIRouter()

class PolicyResponse(BaseModel):
    policy_number: str
    holder_name: str
    status: str  # Active, Expired, Cancelled
    vehicle_info: str
    coverage_limit: float
    deductible: float
    effective_date: str
    expiration_date: str

# Mock Database
MOCK_POLICIES = {
    "POL-123456789": {
        "policy_number": "POL-123456789",
        "holder_name": "John Doe",
        "status": "Active",
        "vehicle_info": "2022 Tesla Model 3",
        "coverage_limit": 50000.0,
        "deductible": 500.0,
        "effective_date": "2024-01-01",
        "expiration_date": "2025-01-01"
    },
    "POL-987654321": {
        "policy_number": "POL-987654321",
        "holder_name": "Jane Smith",
        "status": "Expired",
        "vehicle_info": "2019 Honda Civic",
        "coverage_limit": 30000.0,
        "deductible": 1000.0,
        "effective_date": "2023-01-01",
        "expiration_date": "2024-01-01"
    }
}

logger = logging.getLogger(__name__)
redis_client = None

@router.on_event("startup")
async def startup_event():
    global redis_client
    try:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        # Attempt a ping to ensure the connection works, but don't crash if redis is unavailable
        await redis_client.ping()
        logger.info("Successfully connected to Redis cache")
    except Exception as e:
        logger.warning(f"Failed to connect to Redis cache: {e}. Caching will be disabled.")
        redis_client = None

@router.on_event("shutdown")
async def shutdown_event():
    global redis_client
    if redis_client:
        await redis_client.close()


@router.get("/{policy_number}", response_model=PolicyResponse, dependencies=[Depends(get_api_key)])
async def get_policy(policy_number: str):
    """
    Mock endpoint to retrieve policy details with Redis caching.
    """
    cache_key = f"policy:{policy_number}"

    if redis_client:
        try:
            cached_policy = await redis_client.get(cache_key)
            if cached_policy:
                return json.loads(cached_policy)
        except Exception as e:
            logger.warning(f"Redis get failed: {e}")

    # Fallback to Mock Database if not cached
    policy = MOCK_POLICIES.get(policy_number)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    if redis_client:
        try:
            # Cache the policy for 1 hour (3600 seconds)
            await redis_client.setex(cache_key, 3600, json.dumps(policy))
        except Exception as e:
            logger.warning(f"Redis set failed: {e}")

    return policy
