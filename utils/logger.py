import logging
import sys
from logging.handlers import RotatingFileHandler

from .config import settings

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

# Create a rotating file handler
file_handler = RotatingFileHandler("app.log", maxBytes=1024 * 1024 * 10, backupCount=5)
file_handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)

# Add a console handler for debug logs
if logger.level == logging.DEBUG:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)