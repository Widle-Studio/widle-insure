import os

import pytest

# Set environment variable before importing app to configure CORS for tests
os.environ["BACKEND_CORS_ORIGINS"] = '["http://localhost:3000"]'

@pytest.fixture(autouse=True)
def _setup_cors_env():
    # Make sure we use the right setting for this test
    # (FastAPI tests might share state, we should probably force reload the app if needed,
    # but setting env should be sufficient if we also reset the origin list if it is a dynamic router)
    # The actual issue is that config was already loaded from .env when we run pytest.
    pass

from fastapi.testclient import TestClient


def test_cors_preflight():
    from importlib import reload

    import app.core.config
    os.environ["BACKEND_CORS_ORIGINS"] = '["http://localhost:3000"]'
    reload(app.core.config)
    import app.main
    reload(app.main)
    client = TestClient(app.main.app)
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
    from importlib import reload

    import app.core.config
    os.environ["BACKEND_CORS_ORIGINS"] = '["http://localhost:3000"]'
    reload(app.core.config)
    import app.main
    reload(app.main)
    client = TestClient(app.main.app)

    response = client.options(
        "/health",
        headers={
            "Origin": "http://malicious-site.com",
            "Access-Control-Request-Method": "GET",
        }
    )

    # FastAPI returns 200/400 for CORS preflight, but does not include the CORS headers if origin is blocked
    assert "access-control-allow-origin" not in response.headers
