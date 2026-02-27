import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.claims import Claim
from app.schemas.claims import ClaimCreate
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_create_claim(client: AsyncClient, db: AsyncSession):
    claim_data = {
        "policy_number": "POL-123456789",
        "incident_date": "2024-01-01T10:00:00",
        "incident_location": "123 Main St",
        "incident_description": "Rear-end collision",
        "vehicle_vin": "VIN123456789",
        "vehicle_make": "Toyota",
        "vehicle_model": "Camry",
        "vehicle_year": 2020,
        "claimant_name": "John Doe",
        "claimant_email": "john.doe@example.com",
        "claimant_phone": "555-0100"
    }

    response = await client.post("/api/v1/claims/", json=claim_data)
    assert response.status_code == 200
    data = response.json()
    assert data["policy_number"] == claim_data["policy_number"]
    assert "id" in data
    assert "claim_number" in data

@pytest.mark.asyncio
async def test_get_claim(client: AsyncClient, db: AsyncSession):
    # First, create a claim
    claim_data = {
        "policy_number": "POL-987654321",
        "incident_date": "2024-02-01T15:00:00",
        "incident_location": "456 Elm St",
        "incident_description": "Side-swipe",
        "vehicle_year": 2022,
        "claimant_name": "Jane Doe",
        "claimant_email": "jane.doe@example.com",
        "claimant_phone": "555-0101"
    }
    create_response = await client.post("/api/v1/claims/", json=claim_data)
    claim_id = create_response.json()["id"]

    # Now, retrieve the claim
    response = await client.get(f"/api/v1/claims/{claim_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == claim_id
    assert data["policy_number"] == claim_data["policy_number"]

@pytest.mark.asyncio
async def test_upload_photo(client: AsyncClient, db: AsyncSession):
    # Create claim
    claim_data = {
        "policy_number": "POL-PHOTO-TEST",
        "incident_date": "2024-03-01T12:00:00",
        "incident_location": "789 Pine St",
        "incident_description": "Bumper damage",
        "vehicle_year": 2023,
        "claimant_name": "Photo User",
        "claimant_email": "photo@example.com",
        "claimant_phone": "555-0102"
    }
    create_response = await client.post("/api/v1/claims/", json=claim_data)
    claim_id = create_response.json()["id"]

    # Mock storage service to avoid writing to disk
    with patch("app.services.storage.storage_service.upload_file", new_callable=AsyncMock) as mock_upload:
        mock_upload.return_value = "uploads/test_image.jpg"

        # Create dummy file
        files = {'file': ('test_image.jpg', b'fake_image_content', 'image/jpeg')}

        response = await client.post(f"/api/v1/claims/{claim_id}/photos", files=files)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "photo_url" in data
        assert data["photo_url"] == "uploads/test_image.jpg"

        # Verify photo retrieval with claim
        get_response = await client.get(f"/api/v1/claims/{claim_id}")
        claim_data = get_response.json()
        assert len(claim_data["photos"]) == 1
        assert claim_data["photos"][0]["id"] == data["id"]
