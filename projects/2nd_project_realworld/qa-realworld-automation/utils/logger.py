import logging
import os
from datetime import datetime
from config.config import LOG_DIR, LOG_LEVEL

def setup_logger(name="test_logger"):
    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"log_{timestamp}.log")

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger