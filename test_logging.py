import logging
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.core.logging import setup_logging

def test_logging():
    setup_logging()
    logger = logging.getLogger("test_logger")
    logger.info("This is an info message from the test script.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")

if __name__ == "__main__":
    test_logging()
