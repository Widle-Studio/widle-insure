from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
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

@router.get("/{policy_number}", response_model=PolicyResponse, dependencies=[Depends(get_api_key)])
async def get_policy(policy_number: str):
    """
    Mock endpoint to retrieve policy details.
    """
    policy = MOCK_POLICIES.get(policy_number)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy
