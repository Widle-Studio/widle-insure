import logging
import asyncio

import resend

from app.core.config import settings

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        if getattr(settings, "RESEND_API_KEY", None):
            resend.api_key = getattr(settings, "RESEND_API_KEY", None)
            self.enabled = True
        else:
            self.enabled = False

    async def send_email(self, to: str, subject: str, body: str) -> None:
        """
        Sends an email using Resend SDK, or logs mock output if API key is not set.
        """
        if self.enabled:
            logger.info(f"Sending real email to {to} via Resend...")
            try:
                # Wrap sync resend call in an async thread to prevent blocking FastAPI's event loop
                params = {
                    "from": getattr(settings, "EMAIL_FROM", "test@example.com"),
                    "to": [to],
                    "subject": subject,
                    "html": body
                }
                email_res = await asyncio.to_thread(resend.Emails.send, params)
                logger.info(f"Email successfully sent. ID: {email_res.get('id', 'unknown')}")
            except Exception as e:
                logger.error(f"Failed to send email to {to} via Resend. Error: {str(e)}")
        else:
            logger.info(f"Mock sending email to: {to}")
            logger.info(f"Subject: {subject}")
            logger.info(f"Body: {body}")
            print(f"--- MOCK EMAIL ---")
            print(f"To: {to}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")
            print(f"------------------")

email_service = EmailService()
