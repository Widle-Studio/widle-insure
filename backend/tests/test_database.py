import pytest
from app.core.database import engine
from app.core.config import settings

def test_database_engine_logging_disabled():
    """
    Test that SQLAlchemy engine logging (echo) is disabled by default.
    This is a critical security control to prevent leaking sensitive data,
    PII, and credentials into application logs.
    """
    assert engine.echo is False, "SQLAlchemy engine echo must be disabled by default"
