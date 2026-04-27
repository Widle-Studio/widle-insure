from unittest.mock import patch

import pytest

from app.services.email import EmailService


@pytest.mark.asyncio
async def test_send_email_success():
    """Test successful email sending with Resend API enabled."""
    with patch("app.services.email.resend") as mock_resend, \
         patch("app.services.email.logger") as mock_logger, \
         patch("app.services.email.getattr") as mock_getattr:

        # Setup getattr to simulate configured settings
        def side_effect(obj, attr, default=None):
            if attr == "RESEND_API_KEY":
                return "test_key"
            if attr == "EMAIL_FROM":
                return "test@example.com"
            return default
        mock_getattr.side_effect = side_effect

        # Initialize service with mocked settings
        service = EmailService()
        assert service.enabled is True

        mock_resend.Emails.send.return_value = {"id": "test_id"}

        await service.send_email("recipient@example.com", "Test Subject", "Test Body")

        mock_resend.Emails.send.assert_called_once()
        mock_logger.info.assert_any_call("Email successfully sent. ID: test_id")

@pytest.mark.asyncio
async def test_send_email_failure():
    """Test error handling when Resend API fails."""
    with patch("app.services.email.resend") as mock_resend, \
         patch("app.services.email.logger") as mock_logger, \
         patch("app.services.email.getattr") as mock_getattr:

        # Setup getattr to simulate configured settings
        mock_getattr.side_effect = lambda obj, attr, default=None: "test_value" if attr in ["RESEND_API_KEY", "EMAIL_FROM"] else default

        service = EmailService()
        assert service.enabled is True

        # Simulate Resend API failure
        mock_resend.Emails.send.side_effect = Exception("Resend API Error")

        await service.send_email("recipient@example.com", "Test Subject", "Test Body")

        mock_resend.Emails.send.assert_called_once()
        mock_logger.error.assert_called_once_with(
            "Failed to send email to recipient@example.com via Resend. Error: Resend API Error"
        )

@pytest.mark.asyncio
async def test_send_email_disabled():
    """Test mock email sending when Resend API is disabled."""
    with patch("app.services.email.logger") as mock_logger, \
         patch("app.services.email.getattr") as mock_getattr:

        # Setup getattr to simulate missing API key
        mock_getattr.return_value = None

        service = EmailService()
        assert service.enabled is False

        await service.send_email("recipient@example.com", "Test Subject", "Test Body")

        mock_logger.info.assert_any_call("Mock sending email to: recipient@example.com")
        mock_logger.info.assert_any_call("Subject: Test Subject")
        mock_logger.info.assert_any_call("Body: Test Body")
