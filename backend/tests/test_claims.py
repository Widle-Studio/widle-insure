import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.config import settings

@pytest.mark.asyncio
async def test_create_claim_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            f"{settings.API_V1_STR}/claims/",
            json={
                "policy_number": "POL-12345",
                "incident_date": "2023-01-01T10:00:00Z",
                "incident_location": "123 Main St, Anytown",
                "incident_description": "Rear-ended at a stoplight.",
                "vehicle_vin": "1HGCM82633A000000",
                "vehicle_make": "Honda",
                "vehicle_model": "Accord",
                "vehicle_year": 2018,
                "claimant_name": "John Doe",
                "claimant_email": "john.doe@example.com",
                "claimant_phone": "555-1234"
            },
            headers={"x-api-key": settings.API_KEY}
        )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["policy_number"] == "POL-12345"
    assert data["status"] == "New"
    assert data["claim_number"].startswith(f"CLM-")

@pytest.mark.asyncio
async def test_create_claim_invalid_email():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            f"{settings.API_V1_STR}/claims/",
            json={
                "policy_number": "POL-12345",
                "incident_date": "2023-01-01T10:00:00Z",
                "incident_location": "123 Main St, Anytown",
                "incident_description": "Rear-ended at a stoplight.",
                "vehicle_vin": "1HGCM82633A000000",
                "vehicle_make": "Honda",
                "vehicle_model": "Accord",
                "vehicle_year": 2018,
                "claimant_name": "John Doe",
                "claimant_email": "invalid-email",
                "claimant_phone": "555-1234"
            },
            headers={"x-api-key": settings.API_KEY}
        )
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "claimant_email"]

@pytest.mark.asyncio
async def test_create_claim_future_date():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            f"{settings.API_V1_STR}/claims/",
            json={
                "policy_number": "POL-12345",
                "incident_date": "2030-01-01T10:00:00Z",
                "incident_location": "123 Main St, Anytown",
                "incident_description": "Rear-ended at a stoplight.",
                "vehicle_vin": "1HGCM82633A000000",
                "vehicle_make": "Honda",
                "vehicle_model": "Accord",
                "vehicle_year": 2018,
                "claimant_name": "John Doe",
                "claimant_email": "john.doe@example.com",
                "claimant_phone": "555-1234"
            },
            headers={"x-api-key": settings.API_KEY}
        )
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "incident_date"]
