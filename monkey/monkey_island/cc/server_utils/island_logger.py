import logging
import logging.handlers
import sys
from pathlib import Path

ISLAND_LOG_FILENAME = "monkey_island.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s() - %(message)s"
FILE_MAX_BYTES = 10485760
FILE_BACKUP_COUNT = 20
FILE_ENCODING = "utf8"


def setup_logging(data_dir: Path, log_level: str):
    """
    Set up the logger

    :param data_dir: The data directory
    :param log_level: A string representing threshold for the logger. Valid values are "DEBUG",
                      "INFO", "WARNING", "ERROR", and "CRITICAL".
    """
    logger = logging.getLogger()
    logger.setLevel(log_level.upper())

    formatter = _get_log_formatter()

    log_file_path = get_log_file_path(data_dir)
    _add_file_handler(logger, formatter, log_file_path)

    _add_console_handler(logger, formatter)


def get_log_file_path(data_dir: Path) -> Path:
    return data_dir / ISLAND_LOG_FILENAME


def setup_default_failsafe_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = _get_log_formatter()

    _add_console_handler(logger, formatter)


def _get_log_formatter():
    return logging.Formatter(LOG_FORMAT)


def _add_file_handler(logger, formatter, file_path):
    fh = logging.handlers.RotatingFileHandler(
        file_path, maxBytes=FILE_MAX_BYTES, backupCount=FILE_BACKUP_COUNT, encoding=FILE_ENCODING
    )
    fh.setFormatter(formatter)

    logger.addHandler(fh)


def _add_console_handler(logger, formatter):
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setFormatter(formatter)

    logger.addHandler(ch)


def reset_logger():
    logger = logging.getLogger()

    for handler in logger.handlers:
        logger.removeHandler(handler)
