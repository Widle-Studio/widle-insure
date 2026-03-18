"""
Tests for security and API key validation functions.
"""

import pytest
from fastapi import HTTPException

from app.core.config import settings

# pylint: disable=import-error
from app.core.security import get_api_key


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
async def test_get_api_key_invalid_input():
    """
    Directly test that get_api_key with invalid input raises a 403 Forbidden HTTPException.
    """
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(api_key="invalid_input")

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Could not validate credentials"

@pytest.mark.asyncio
async def test_get_api_key_same_length_invalid():
    """
    Test that an invalid API key of the exact same length as the valid one
    raises a 403 Forbidden HTTPException. This tests the timing-attack protection
    scenario for secrets.compare_digest.
    """
    valid_key = settings.API_KEY
    if not valid_key:
        valid_key = "test_key"

    # Create an invalid key of the same length by changing the last character
    invalid_char = "b" if valid_key[-1] == "a" else "a"
    same_length_invalid_key = valid_key[:-1] + invalid_char

    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(api_key=same_length_invalid_key)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Could not validate credentials"

@pytest.mark.asyncio
async def test_get_api_key_valid():
    """
    Test that a valid API key is correctly returned.
    """
    result = await get_api_key(api_key=settings.API_KEY)
    assert result == settings.API_KEY

@pytest.mark.asyncio
async def test_get_api_key_partial_match():
    """
    Test that a partially matching API key (e.g. prefix) raises 403.
    """
    partial_key = (
        settings.API_KEY[:-1]
        if settings.API_KEY and len(settings.API_KEY) > 1
        else "partial"
    )
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(api_key=partial_key)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Could not validate credentials"
