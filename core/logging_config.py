import logging
import sys
import os

def setup_logging(log_file="friday.log"):
    logger = logging.getLogger("Friday")
    logger.setLevel(logging.INFO)

    # Standard format for log aggregation
    formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'
    )

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# Initialize global logger
friday_logger = setup_logging()
