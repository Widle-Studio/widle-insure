from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Widle Insure API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "supersecretkey"
    
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "insurance_claims"
    DATABASE_URL: Optional[str] = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return "sqlite+aiosqlite:///./sql_app.db"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
