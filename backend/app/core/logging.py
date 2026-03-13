import logging as std_logging
import sys


def setup_logging():
    """
    Configure logging for the application.
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    std_logging.basicConfig(
        level=std_logging.INFO,
        format=log_format,
        handlers=[
            std_logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set log levels for third-party libraries
    std_logging.getLogger("uvicorn.access").setLevel(std_logging.INFO)
    std_logging.getLogger("sqlalchemy.engine").setLevel(std_logging.WARNING)
