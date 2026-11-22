
import logging
from pathlib import Path


def setup_logger(name="GeoPulse"):
    log_directory = Path("data/logs")
    log_directory.mkdir(parents=True, exist_ok=True)

    log_file = log_directory / "gps_pipeline.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )

        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
