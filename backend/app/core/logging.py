import logging
import sys
from app.core.config import settings

def setup_logging():
    """
    Configure logging for the application.
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set log levels for third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    # Example of structured logging setup (if needed in future)
    # import structlog
    # ...
