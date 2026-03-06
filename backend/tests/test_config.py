import pytest
from pydantic import ValidationError


def test_missing_postgres_password_raises_error(monkeypatch):
    """
    Test that missing POSTGRES_PASSWORD environment variable raises a validation error.
    This ensures the security fix to remove the hardcoded password remains in place.
    """
    # Temporarily remove POSTGRES_PASSWORD from the environment if it exists
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)

    # Also patch out the .env file loading since Settings reads from .env

    # We must delay the import of Settings to inside the test so it picks up the patched env
    from app.core.config import Settings

    # Pydantic loads from `.env` file because `env_file = ".env"` is defined in the Config.
    # We can override this by passing _env_file=None
    with pytest.raises(ValidationError) as excinfo:
        Settings(_env_file=None)

    # Check that POSTGRES_PASSWORD is among the missing fields in the validation error
    error_msg = str(excinfo.value)
    assert "POSTGRES_PASSWORD\n  Field required" in error_msg
