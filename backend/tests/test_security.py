import pytest
from fastapi import HTTPException

from app.core.security import get_api_key
from app.core.config import settings

@pytest.mark.asyncio
async def test_get_api_key_invalid():
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(api_key="invalid_key")

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Could not validate credentials"

@pytest.mark.asyncio
async def test_get_api_key_missing():
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(api_key=None)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Could not validate credentials"

@pytest.mark.asyncio
async def test_get_api_key_valid():
    result = await get_api_key(api_key=settings.API_KEY)
    assert result == settings.API_KEY

@pytest.mark.asyncio
async def test_get_api_key_empty():
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(api_key="")

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Could not validate credentials"
