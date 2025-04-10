"""
Logging configuration module.

This module provides a centralized configuration for logging in the application,
using the LOG_LEVEL from environment settings with colored output.
"""
import logging
import sys
from typing import Dict
from src.business_assistant.config.env import settings

# ANSI color codes for terminal output
COLORS = {
    'RESET': '\033[0m',
    'BLACK': '\033[30m',
    'RED': '\033[31m',
    'GREEN': '\033[32m',
    'YELLOW': '\033[33m',
    'BLUE': '\033[34m',
    'MAGENTA': '\033[35m',
    'CYAN': '\033[36m',
    'WHITE': '\033[37m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
}

# Color mapping for different log levels
LEVEL_COLORS = {
    'DEBUG': COLORS['BLUE'],
    'INFO': COLORS['GREEN'],
    'WARNING': COLORS['YELLOW'],
    'ERROR': COLORS['RED'],
    'CRITICAL': COLORS['BOLD'] + COLORS['RED'],
}


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log messages based on level."""
    
    def format(self, record):
        # Get the original formatted message
        log_message = super().format(record)
        
        # Add color based on the log level if available
        level_name = record.levelname
        if level_name in LEVEL_COLORS:
            return f"{LEVEL_COLORS[level_name]}{log_message}{COLORS['RESET']}"
        
        return log_message


# Define a colored formatter for consistent log message formatting
colored_formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a handler for stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(colored_formatter)

# Dictionary to store initialized loggers
_loggers: Dict[str, logging.Logger] = {}


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger with the specified name and colored output.
    Uses a singleton pattern to ensure each named logger is only initialized once.
    
    Args:
        name: The name for the logger, typically the module name.
        
    Returns:
        A configured logger instance with colored output.
    """
    # Check if this logger has already been initialized
    if name in _loggers:
        return _loggers[name]
    
    # Get a new logger
    logger = logging.getLogger(name)
    
    # Set the log level from environment settings
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Remove any existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Add the console handler with colored output
    logger.addHandler(console_handler)
    
    # Store the logger in our dictionary
    _loggers[name] = logger
    
    return logger
