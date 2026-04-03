import uuid
import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch, MagicMock

from app.core.config import settings
from app.core.database import get_db
from app.main import app

@pytest.mark.asyncio
async def test_analyze_claim_not_found():
    auth_headers = {"x-api-key": settings.API_KEY}
    claim_id = uuid.uuid4()

    # Mock db.execute to return None for first()
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            f"{settings.API_V1_STR}/claims/{claim_id}/analyze",
            headers=auth_headers,
        )

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["detail"] == "Claim not found"

@pytest.mark.asyncio
async def test_analyze_claim_no_photos(mock_claim_class):
    auth_headers = {"x-api-key": settings.API_KEY}
    claim_id = uuid.uuid4()

    mock_claim = mock_claim_class(claim_id, {})
    mock_claim.photos = []

    # Mock db.execute to return the claim with no photos
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_claim
    mock_db.execute.return_value = mock_result

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            f"{settings.API_V1_STR}/claims/{claim_id}/analyze",
            headers=auth_headers,
        )

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json()["detail"] == "No photos to analyze"
