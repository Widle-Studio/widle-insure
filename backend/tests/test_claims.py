from datetime import datetime, timezone

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.main import app


@pytest.fixture
def valid_claim_payload():
    return {
        "policy_number": "POL-123456789",
        "incident_date": "2024-01-01T12:00:00",
        "incident_location": "New York, NY",
        "incident_description": "Fender bender at intersection",
        "vehicle_vin": "1HGCM82633A004123",
        "vehicle_make": "Honda",
        "vehicle_model": "Accord",
        "vehicle_year": 2022,
        "claimant_name": "John Doe",
        "claimant_email": "john.doe@example.com",
        "claimant_phone": "555-0123",
    }


@pytest.mark.asyncio
async def test_create_claim_unauthorized(valid_claim_payload: dict):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            f"{settings.API_V1_STR}/claims/", json=valid_claim_payload
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_claim_missing_required_fields(valid_claim_payload: dict):
    invalid_payload = valid_claim_payload.copy()
    del invalid_payload["policy_number"]

    auth_headers = {"x-api-key": settings.API_KEY}
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            f"{settings.API_V1_STR}/claims/", json=invalid_payload, headers=auth_headers
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_claim_success(valid_claim_payload: dict):
    from app.core.database import get_db

    auth_headers = {"x-api-key": settings.API_KEY}

    # Mocking the database session instead of spinning up sqlite+aiosqlite which hangs
    class MockDbSession:
        def __init__(self):
            self.added = []

        def add(self, item):
            self.added.append(item)

        async def commit(self):
            pass

        async def refresh(self, item):
            item.id = "123e4567-e89b-12d3-a456-426614174000"
            item.created_at = datetime.now(timezone.utc)
            item.updated_at = datetime.now(timezone.utc)
            pass

        async def execute(self, stmt):
            class MockResult:
                def scalars(inner_self):
                    class MockScalars:
                        def first(self2):
                            return self.added[0]

                    return MockScalars()

            return MockResult()

    mock_db = MockDbSession()

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                f"{settings.API_V1_STR}/claims/",
                json=valid_claim_payload,
                headers=auth_headers,
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["policy_number"] == valid_claim_payload["policy_number"]
    assert data["status"] == "New"
    assert "claim_number" in data
    assert data["claim_number"].startswith("CLM-")

    # Verify the mock db received the item
    assert len(mock_db.added) == 1
    db_claim = mock_db.added[0]
    assert db_claim.policy_number == valid_claim_payload["policy_number"]
    assert db_claim.status == "New"


@pytest.mark.asyncio
async def test_upload_claim_photo_invalid_content_type():
    auth_headers = {"x-api-key": settings.API_KEY}

    # We create a fake text file with a .jpg extension
    fake_file_content = b"This is just a text file, not an image."

    files = {"file": ("fake_image.jpg", fake_file_content, "image/jpeg")}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # The endpoint expects /claims/{claim_id}/photos
        claim_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.post(
            f"{settings.API_V1_STR}/claims/{claim_id}/photos",
            files=files,
            headers=auth_headers,
        )

    assert response.status_code == 400
    assert "Invalid file content type" in response.json()["detail"]


@pytest.mark.asyncio
async def test_upload_claim_photo_invalid_file_extension():
    auth_headers = {"x-api-key": settings.API_KEY}

    # valid jpeg bytes
    valid_jpeg_content = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00"

    # Give it an invalid extension .pdf
    files = {"file": ("fake_image.pdf", valid_jpeg_content, "image/jpeg")}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        claim_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.post(
            f"{settings.API_V1_STR}/claims/{claim_id}/photos",
            files=files,
            headers=auth_headers,
        )

    assert response.status_code == 400
    assert "Invalid file extension" in response.json()["detail"]


@pytest.mark.asyncio
async def test_upload_claim_photo_claim_not_found():
    from app.core.database import get_db

    auth_headers = {"x-api-key": settings.API_KEY}
    valid_jpeg_content = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00"
    files = {"file": ("real_image.jpg", valid_jpeg_content, "image/jpeg")}

    class MockDbSession:
        async def execute(self, stmt):
            class MockResult:
                def scalars(inner_self):
                    class MockScalars:
                        def first(self2):
                            return None
                    return MockScalars()
            return MockResult()

    mock_db = MockDbSession()

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            claim_id = "123e4567-e89b-12d3-a456-426614174000"
            response = await client.post(
                f"{settings.API_V1_STR}/claims/{claim_id}/photos",
                files=files,
                headers=auth_headers,
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert "Claim not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_upload_claim_photo_success():
    from unittest.mock import AsyncMock, patch
    from app.core.database import get_db

    auth_headers = {"x-api-key": settings.API_KEY}
    valid_jpeg_content = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00"
    files = {"file": ("real_image.jpg", valid_jpeg_content, "image/jpeg")}

    class DummyClaim:
        id = "123e4567-e89b-12d3-a456-426614174000"

    class MockDbSession:
        def __init__(self):
            self.added = []

        def add(self, item):
            self.added.append(item)

        async def commit(self):
            pass

        async def refresh(self, item):
            item.id = "550e8400-e29b-41d4-a716-446655440000"
            item.created_at = datetime.now(timezone.utc)
            item.updated_at = datetime.now(timezone.utc)

        async def execute(self, stmt):
            class MockResult:
                def scalars(inner_self):
                    class MockScalars:
                        def first(self2):
                            return DummyClaim()
                    return MockScalars()
            return MockResult()

    mock_db = MockDbSession()

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with patch("app.api.v1.endpoints.claims.storage_service.upload_file", new_callable=AsyncMock) as mock_upload_file:
            mock_upload_file.return_value = "/mock/path/real_image.jpg"

            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                claim_id = "123e4567-e89b-12d3-a456-426614174000"
                response = await client.post(
                    f"{settings.API_V1_STR}/claims/{claim_id}/photos",
                    files=files,
                    headers=auth_headers,
                )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "550e8400-e29b-41d4-a716-446655440000"
    assert data["photo_url"] == "/mock/path/real_image.jpg"
    assert "description" in data

    # Verify db interaction
    import uuid
    assert len(mock_db.added) == 1
    added_photo = mock_db.added[0]
    assert added_photo.claim_id == uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    assert added_photo.photo_url == "/mock/path/real_image.jpg"
    assert added_photo.photo_type == "image/jpeg"
