import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.main import app


@pytest.mark.asyncio
async def test_get_policy_success():
    transport = ASGITransport(app=app)
    headers = {"x-api-key": settings.API_KEY}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"{settings.API_V1_STR}/policies/POL-123456789", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["policy_number"] == "POL-123456789"
    assert data["holder_name"] == "John Doe"
    assert data["status"] == "Active"


@pytest.mark.asyncio
async def test_get_policy_not_found():
    transport = ASGITransport(app=app)
    headers = {"x-api-key": settings.API_KEY}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"{settings.API_V1_STR}/policies/POL-NONEXISTENT", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Policy not found"


@pytest.mark.asyncio
async def test_get_policy_unauthorized():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"{settings.API_V1_STR}/policies/POL-123456789")
    assert response.status_code == 403
    assert response.json()["detail"] == "Could not validate credentials"
