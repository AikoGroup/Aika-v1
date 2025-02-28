"""
Logging utilities for the Aika AI System.
"""

import logging
import sys
from typing import Optional

from .config import get_settings

# Get settings
settings = get_settings()

# Define log levels
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

# Configure root logger
def configure_logging(log_level: Optional[str] = None) -> None:
    """
    Configure the root logger.
    
    Args:
        log_level: Log level (defaults to settings.LOG_LEVEL)
    """
    if log_level is None:
        log_level = settings.LOG_LEVEL
        
    level = LOG_LEVELS.get(log_level.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Set log levels for third-party libraries
    logging.getLogger("uvicorn").setLevel(level)
    logging.getLogger("fastapi").setLevel(level)
    
    # Set lower log level for noisy libraries
    if level <= logging.INFO:
        logging.getLogger("kafka").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
