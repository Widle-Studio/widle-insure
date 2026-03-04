import logging
import sys
from unittest.mock import patch, MagicMock
from app.core.logging import setup_logging

def test_setup_logging_configures_basic_config():
    """
    Test that setup_logging configures basicConfig correctly and sets
    the expected format and handlers.
    """
    with patch("app.core.logging.logging.basicConfig") as mock_basic_config, \
         patch("app.core.logging.logging.getLogger") as mock_get_logger:

        setup_logging()

        # Verify basicConfig was called correctly
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        mock_basic_config.assert_called_once()
        call_kwargs = mock_basic_config.call_args.kwargs

        assert call_kwargs["level"] == logging.INFO
        assert call_kwargs["format"] == log_format
        assert len(call_kwargs["handlers"]) == 1

        handler = call_kwargs["handlers"][0]
        assert isinstance(handler, logging.StreamHandler)
        assert handler.stream == sys.stdout

def test_setup_logging_configures_third_party_loggers():
    """
    Test that setup_logging configures specific levels for third-party loggers.
    """
    with patch("app.core.logging.logging.basicConfig"), \
         patch("app.core.logging.logging.getLogger") as mock_get_logger:

        # We need to mock the loggers returned by getLogger so we can check setLevel
        uvicorn_logger_mock = MagicMock()
        sqlalchemy_logger_mock = MagicMock()

        def get_logger_side_effect(name):
            if name == "uvicorn.access":
                return uvicorn_logger_mock
            elif name == "sqlalchemy.engine":
                return sqlalchemy_logger_mock
            return MagicMock()

        mock_get_logger.side_effect = get_logger_side_effect

        setup_logging()

        # Verify setLevel was called with correct levels
        uvicorn_logger_mock.setLevel.assert_called_once_with(logging.INFO)
        sqlalchemy_logger_mock.setLevel.assert_called_once_with(logging.WARNING)
