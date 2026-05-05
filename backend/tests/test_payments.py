import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import stripe
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.database import get_db
from app.main import app


@pytest.mark.asyncio
async def test_initiate_payout_unauthorized():
    transport = ASGITransport(app=app)
    claim_id = uuid.uuid4()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(f"{settings.API_V1_STR}/payments/{claim_id}/payout")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_initiate_payout_claim_not_found():
    auth_headers = {"x-api-key": settings.API_KEY}
    claim_id = uuid.uuid4()

    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            f"{settings.API_V1_STR}/payments/{claim_id}/payout",
            headers=auth_headers,
        )

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["detail"] == "Claim not found"


@pytest.mark.asyncio
async def test_initiate_payout_claim_not_approved(mock_claim_class):
    auth_headers = {"x-api-key": settings.API_KEY}
    claim_id = uuid.uuid4()

    mock_claim = mock_claim_class(claim_id, {})
    mock_claim.status = "New"

    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_claim
    mock_db.execute.return_value = mock_result

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            f"{settings.API_V1_STR}/payments/{claim_id}/payout",
            headers=auth_headers,
        )

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json()["detail"] == "Only approved claims can be paid out"


@pytest.mark.asyncio
async def test_initiate_payout_amount_zero(mock_claim_class):
    auth_headers = {"x-api-key": settings.API_KEY}
    claim_id = uuid.uuid4()

    mock_claim = mock_claim_class(claim_id, {})
    mock_claim.status = "Approved"
    mock_claim.approved_amount = 0

    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_claim
    mock_db.execute.return_value = mock_result

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    with patch("app.api.v1.endpoints.payments.getattr") as mock_getattr:
        mock_getattr.side_effect = lambda obj, attr, default=None: "test_stripe_key" if attr == "STRIPE_SECRET_KEY" else getattr(obj, attr, default)

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                f"{settings.API_V1_STR}/payments/{claim_id}/payout",
                headers=auth_headers,
            )

    app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error during payout"


@pytest.mark.asyncio
async def test_initiate_payout_stripe_success(mock_claim_class):
    auth_headers = {"x-api-key": settings.API_KEY}
    claim_id = uuid.uuid4()

    mock_claim = mock_claim_class(claim_id, {})
    mock_claim.status = "Approved"
    mock_claim.approved_amount = 1000.00

    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_claim
    mock_db.execute.return_value = mock_result

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    with patch("app.api.v1.endpoints.payments.getattr") as mock_getattr, \
         patch("stripe.Transfer.create") as mock_transfer_create:

        mock_getattr.side_effect = lambda obj, attr, default=None: "test_stripe_key" if attr == "STRIPE_SECRET_KEY" else getattr(obj, attr, default)

        mock_transfer = MagicMock()
        mock_transfer.id = "tr_123456"
        mock_transfer_create.return_value = mock_transfer

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                f"{settings.API_V1_STR}/payments/{claim_id}/payout",
                headers=auth_headers,
            )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert mock_claim.status == "Paid"
    mock_transfer_create.assert_called_once_with(
        amount=100000,
        currency="usd",
        destination="acct_1032D82eZvKYlo2C",
        description=f"Insurance claim payout: {mock_claim.claim_number}"
    )


@pytest.mark.asyncio
async def test_initiate_payout_mock_success(mock_claim_class):
    auth_headers = {"x-api-key": settings.API_KEY}
    claim_id = uuid.uuid4()

    mock_claim = mock_claim_class(claim_id, {})
    mock_claim.status = "Approved"
    mock_claim.approved_amount = 1000.00

    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_claim
    mock_db.execute.return_value = mock_result

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    with patch("app.api.v1.endpoints.payments.getattr") as mock_getattr:
        mock_getattr.side_effect = lambda obj, attr, default=None: None if attr == "STRIPE_SECRET_KEY" else getattr(obj, attr, default)

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                f"{settings.API_V1_STR}/payments/{claim_id}/payout",
                headers=auth_headers,
            )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert mock_claim.status == "Paid"


@pytest.mark.asyncio
async def test_initiate_payout_stripe_error(mock_claim_class):
    auth_headers = {"x-api-key": settings.API_KEY}
    claim_id = uuid.uuid4()

    mock_claim = mock_claim_class(claim_id, {})
    mock_claim.status = "Approved"
    mock_claim.approved_amount = 1000.00

    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_claim
    mock_db.execute.return_value = mock_result

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    with patch("app.api.v1.endpoints.payments.getattr") as mock_getattr, \
         patch("stripe.Transfer.create") as mock_transfer_create:

        mock_getattr.side_effect = lambda obj, attr, default=None: "test_stripe_key" if attr == "STRIPE_SECRET_KEY" else getattr(obj, attr, default)

        # Override the property
        class MockStripeError(stripe.error.StripeError):
            @property
            def user_message(self):
                return "Test user message"

        mock_transfer_create.side_effect = MockStripeError("Test Error")

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                f"{settings.API_V1_STR}/payments/{claim_id}/payout",
                headers=auth_headers,
            )

    app.dependency_overrides.clear()

    assert response.status_code == 502
    assert response.json()["detail"] == "Payment gateway error: Test user message"
