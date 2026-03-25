from typing import List, Optional, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Widle Insure API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str # No default value, required from environment
    API_KEY: str # No default value, required from environment
    FIRST_ADMIN_EMAIL: str = "admin@widle.com"
    FIRST_ADMIN_PASSWORD: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # CORS Origins (default empty list, allowing strict configuration)
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = []

    DEBUG: bool = False

    # Maximum upload file size (default 50MB)
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024

    # Sentry DSN for error logging
    SENTRY_DSN: Optional[str] = None

    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[str] = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return "sqlite+aiosqlite:///./sql_app.db"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
