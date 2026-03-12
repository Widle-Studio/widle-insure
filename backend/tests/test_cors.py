import os

# Set environment variable before importing app to configure CORS for tests
os.environ["BACKEND_CORS_ORIGINS"] = '["http://localhost:3000"]'

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_cors_preflight():
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        }
    )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"

def test_cors_rejected_origin():
    response = client.options(
        "/health",
        headers={
            "Origin": "http://malicious-site.com",
            "Access-Control-Request-Method": "GET",
        }
    )

    # FastAPI returns 200/400 for CORS preflight, but does not include the CORS headers if origin is blocked
    assert "access-control-allow-origin" not in response.headers
