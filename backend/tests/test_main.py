import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_root_endpoint_async():
    """Asynchronously test the root endpoint for a successful response."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Widle Insure API"}

@pytest.mark.asyncio
async def test_health_check_async():
    """Asynchronously test the health check endpoint for system status."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "widle-insure-backend"}

def test_read_root():
    """Test the root endpoint for a successful response and correct message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Widle Insure API"}

def test_health_check():
    """Test the health check endpoint for system status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "widle-insure-backend"}
