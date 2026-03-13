import logging  # pylint: disable=import-self
import sys


def setup_logging():
    """
    Configure logging for the application.
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(  # pylint: disable=no-member
        level=logging.INFO,  # pylint: disable=no-member
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)  # pylint: disable=no-member
        ]
    )
    
    # Set log levels for third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)  # pylint: disable=no-member
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)  # pylint: disable=no-member
