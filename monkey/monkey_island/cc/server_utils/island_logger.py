import logging.config
import os
from copy import deepcopy

ISLAND_LOG_FILENAME = "monkey_island.log"

LOGGER_CONFIG_DICT = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(filename)s:%(lineno)s - "
            + "%(funcName)10s() - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "simple",
            "filename": None,  # set in setup_logging()
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8",
        },
    },
    "root": {
        "level": None,  # set in setup_logging()
        "handlers": ["console_handler", "file_handler"],
    },
}


def setup_logging(data_dir_path, log_level):
    """
    Setup the logging configuration
    :param data_dir_path: data directory file path
    :param log_level: level to log from
    :return:
    """

    logger_configuration = deepcopy(LOGGER_CONFIG_DICT)

    logger_configuration["handlers"]["file_handler"]["filename"] = os.path.join(
        data_dir_path, ISLAND_LOG_FILENAME
    )
    logger_configuration["root"]["level"] = log_level.upper()

    logging.config.dictConfig(logger_configuration)
