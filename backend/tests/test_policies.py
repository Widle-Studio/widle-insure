import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.config import settings

@pytest.mark.asyncio
async def test_get_policy_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            f"{settings.API_V1_STR}/policies/POL-12345",
            headers={"x-api-key": settings.API_KEY}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["policy_number"] == "POL-12345"
    assert data["status"] == "Active"

@pytest.mark.asyncio
async def test_get_policy_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            f"{settings.API_V1_STR}/policies/POL-99999",
            headers={"x-api-key": settings.API_KEY}
        )
    assert response.status_code == 404
    assert response.json()["detail"] == "Policy not found"

@pytest.mark.asyncio
async def test_get_policy_expired():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            f"{settings.API_V1_STR}/policies/POL-54321",
            headers={"x-api-key": settings.API_KEY}
        )
    assert response.status_code == 400
    assert "Policy is not active" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_policy_cancelled():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            f"{settings.API_V1_STR}/policies/POL-22222",
            headers={"x-api-key": settings.API_KEY}
        )
    assert response.status_code == 400
    assert "Policy is not active" in response.json()["detail"]
