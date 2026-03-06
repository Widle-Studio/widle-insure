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
    "POL-12345": {
        "policy_number": "POL-12345",
        "holder_name": "John Doe",
        "status": "Active",
        "vehicle_info": "2018 Honda Accord",
        "coverage_limit": 50000.0,
        "deductible": 500.0,
        "effective_date": "2024-01-01",
        "expiration_date": "2025-01-01"
    },
    "POL-54321": {
        "policy_number": "POL-54321",
        "holder_name": "Jane Smith",
        "status": "Expired",
        "vehicle_info": "2015 Toyota Camry",
        "coverage_limit": 30000.0,
        "deductible": 1000.0,
        "effective_date": "2022-01-01",
        "expiration_date": "2023-01-01"
    },
    "POL-11111": {
        "policy_number": "POL-11111",
        "holder_name": "Alice Johnson",
        "status": "Active",
        "vehicle_info": "2021 Ford F-150",
        "coverage_limit": 100000.0,
        "deductible": 250.0,
        "effective_date": "2024-03-01",
        "expiration_date": "2025-03-01"
    },
    "POL-22222": {
        "policy_number": "POL-22222",
        "holder_name": "Bob Williams",
        "status": "Cancelled",
        "vehicle_info": "2019 Chevrolet Malibu",
        "coverage_limit": 25000.0,
        "deductible": 1000.0,
        "effective_date": "2023-05-01",
        "expiration_date": "2024-05-01"
    },
    "POL-33333": {
        "policy_number": "POL-33333",
        "holder_name": "Charlie Brown",
        "status": "Active",
        "vehicle_info": "2020 Subaru Outback",
        "coverage_limit": 50000.0,
        "deductible": 500.0,
        "effective_date": "2024-02-15",
        "expiration_date": "2025-02-15"
    },
    "POL-44444": {
        "policy_number": "POL-44444",
        "holder_name": "Diana Prince",
        "status": "Active",
        "vehicle_info": "2023 Tesla Model Y",
        "coverage_limit": 250000.0,
        "deductible": 1000.0,
        "effective_date": "2024-01-10",
        "expiration_date": "2025-01-10"
    },
    "POL-55555": {
        "policy_number": "POL-55555",
        "holder_name": "Evan Wright",
        "status": "Active",
        "vehicle_info": "2017 Nissan Altima",
        "coverage_limit": 30000.0,
        "deductible": 500.0,
        "effective_date": "2023-08-01",
        "expiration_date": "2024-08-01"
    },
    "POL-66666": {
        "policy_number": "POL-66666",
        "holder_name": "Fiona Gallagher",
        "status": "Expired",
        "vehicle_info": "2014 Jeep Grand Cherokee",
        "coverage_limit": 50000.0,
        "deductible": 500.0,
        "effective_date": "2021-11-01",
        "expiration_date": "2022-11-01"
    },
    "POL-77777": {
        "policy_number": "POL-77777",
        "holder_name": "George Constanza",
        "status": "Active",
        "vehicle_info": "2012 Chrysler Sebring",
        "coverage_limit": 25000.0,
        "deductible": 1000.0,
        "effective_date": "2024-04-01",
        "expiration_date": "2025-04-01"
    },
    "POL-88888": {
        "policy_number": "POL-88888",
        "holder_name": "Hannah Abbott",
        "status": "Active",
        "vehicle_info": "2022 Hyundai Tucson",
        "coverage_limit": 100000.0,
        "deductible": 500.0,
        "effective_date": "2023-12-01",
        "expiration_date": "2024-12-01"
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

    if policy["status"] != "Active":
         raise HTTPException(status_code=400, detail=f"Policy is not active. Current status: {policy['status']}")

    return policy
