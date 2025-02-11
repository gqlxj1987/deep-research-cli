"""Module for handling logging operations"""

import logging
import os
from datetime import datetime
from typing import Optional

class LogUtil:
    """Class for managing logging operations"""

    _instance = None
    _initialized = False

    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super(LogUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize logging configuration"""
        if not LogUtil._initialized:
            self.logger = logging.getLogger('deep_research')
            self.logger.setLevel(logging.DEBUG)
            LogUtil._initialized = True
            self._setup_logging()

    def _setup_logging(self):
        """Setup logging configuration with console handler"""
        # Create formatter
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message: str, *args, **kwargs):
        """Log debug message

        Args:
            message: The message to log
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log info message

        Args:
            message: The message to log
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log warning message

        Args:
            message: The message to log
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log error message

        Args:
            message: The message to log
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log critical message

        Args:
            message: The message to log
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.logger.critical(message, *args, **kwargs)

    @staticmethod
    def get_logger() -> 'LogUtil':
        """Get singleton instance of LogUtil

        Returns:
            LogUtil instance
        """
        return LogUtil()

if __name__ == "__main__":
    # Create logger instance
    logger = LogUtil.get_logger()

    # Example usage of different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")