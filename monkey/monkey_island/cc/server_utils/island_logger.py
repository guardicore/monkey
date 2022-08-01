import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Mapping

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

    log_file_path = data_dir / ISLAND_LOG_FILENAME
    _add_file_handler(logger, formatter, log_file_path)

    _add_console_handler(logger, formatter)


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


def get_log_file() -> Mapping:
    """
    This is a helper function for the Monkey Island log download function.
    It finds the logger handlers and checks if one of them is a fileHandler of any kind by
    checking if the handler has the property handler.baseFilename.

    :return: A dict with log file contents
    """
    logger = logging.getLogger(__name__)

    logger_handlers = logger.parent.handlers
    for handler in logger_handlers:
        if hasattr(handler, "baseFilename"):
            logger.info("Log file found: {0}".format(handler.baseFilename))
            log_file_path = handler.baseFilename
            with open(log_file_path, "rt") as f:
                log_file = f.read()
            return {"log_file": log_file}

    logger.warning("No log file could be found, check logger config.")
    return None
