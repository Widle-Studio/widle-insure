from fastapi.testclient import TestClient
from app.core.config import settings
from app.main import app

client = TestClient(app)
headers = {"x-api-key": settings.API_KEY}

def test_get_policy_success():
    response = client.get(f"{settings.API_V1_STR}/policies/POL-123456789", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"policy_number": "POL-123456789", "holder_name": "John Doe", "status": "Active", "vehicle_info": "2022 Tesla Model 3", "coverage_limit": 50000.0, "deductible": 500.0, "effective_date": "2024-01-01", "expiration_date": "2025-01-01"}

def test_get_policy_not_found():
    response = client.get(f"{settings.API_V1_STR}/policies/POL-NONEXISTENT", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Policy not found"

def test_get_policy_unauthorized():
    response = client.get(f"{settings.API_V1_STR}/policies/POL-123456789")
    assert response.status_code == 403
    assert response.json()["detail"] == "Could not validate credentials"
