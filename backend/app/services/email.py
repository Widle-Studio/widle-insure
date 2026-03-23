import logging

logger = logging.getLogger(__name__)

class EmailService:
    def send_email(self, to: str, subject: str, body: str) -> None:
        """
        Mock email sending service.
        """
        logger.info(f"Mock sending email to: {to}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Body: {body}")
        print(f"--- MOCK EMAIL ---")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print(f"------------------")

email_service = EmailService()
