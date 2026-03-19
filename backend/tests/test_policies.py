import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)
headers = {"x-api-key": settings.API_KEY}

@pytest.mark.parametrize(
    "policy_number, req_headers, expected_status, expected_response",
    [
        (
            "POL-123456789",
            headers,
            200,
            {
                "policy_number": "POL-123456789",
                "holder_name": "John Doe",
                "status": "Active",
                "vehicle_info": "2022 Tesla Model 3",
                "coverage_limit": 50000.0,
                "deductible": 500.0,
                "effective_date": "2024-01-01",
                "expiration_date": "2025-01-01",
            },
        ),
        (
            "POL-987654321",
            headers,
            200,
            {
                "policy_number": "POL-987654321",
                "holder_name": "Jane Smith",
                "status": "Expired",
                "vehicle_info": "2019 Honda Civic",
                "coverage_limit": 30000.0,
                "deductible": 1000.0,
                "effective_date": "2023-01-01",
                "expiration_date": "2024-01-01",
            },
        ),
        (
            "POL-NONEXISTENT",
            headers,
            404,
            {"detail": "Policy not found"},
        ),
        (
            "POL-123456789",
            {},
            403,
            {"detail": "Could not validate credentials"},
        ),
        (
            "POL-123456789",
            {"x-api-key": "invalid-api-key"},
            403,
            {"detail": "Could not validate credentials"},
        ),
    ],
)
def test_get_policy(policy_number, req_headers, expected_status, expected_response):
    response = client.get(f"{settings.API_V1_STR}/policies/{policy_number}", headers=req_headers)
    assert response.status_code == expected_status
    assert response.json() == expected_response
