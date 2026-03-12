import pytest
from fastapi import HTTPException

from app.core.security import get_api_key
from app.core.config import settings

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "invalid_api_key",
    [
        "invalid_key",
        None,
        "",
        "   ",
        "long_invalid_string_that_does_not_match_at_all_1234567890",
        "test_api_key_but_wrong",
    ]
)
async def test_get_api_key_error_paths(invalid_api_key):
    """
    Test that invalid, missing, empty, or whitespace-only API keys
    raise a 403 Forbidden HTTPException.
    """
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(api_key=invalid_api_key)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Could not validate credentials"

@pytest.mark.asyncio
async def test_get_api_key_valid():
    """
    Test that a valid API key is correctly returned.
    """
    result = await get_api_key(api_key=settings.API_KEY)
    assert result == settings.API_KEY
