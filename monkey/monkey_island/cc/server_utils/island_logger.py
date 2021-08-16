import logging
import logging.handlers
import os
import sys

ISLAND_LOG_FILENAME = "monkey_island.log"
LOG_FORMAT = (
    "%(asctime)s - %(filename)s:%(lineno)s - %(funcName)10s() - %(levelname)s - %(message)s"
)
FILE_MAX_BYTES = 10485760
FILE_BACKUP_COUNT = 20
FILE_ENCODING = "utf8"


def setup_logging(data_dir_path, log_level):
    """
    Setup the logging configuration
    :param data_dir_path: data directory file path
    :param log_level: level to log from
    :return:
    """
    logger = logging.getLogger()
    logger.setLevel(log_level.upper())

    formatter = _get_log_formatter()

    log_file_path = os.path.join(data_dir_path, ISLAND_LOG_FILENAME)
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
