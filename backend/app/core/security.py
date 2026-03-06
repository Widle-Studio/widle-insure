from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings
import secrets

api_key_header_scheme = APIKeyHeader(name="x-api-key", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header_scheme)):
    if api_key and secrets.compare_digest(api_key, settings.API_KEY):
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )
