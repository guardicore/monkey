import logging.config
import os
from copy import deepcopy
from typing import Dict

__author__ = "Maor.Rayzin"


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
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": None,  # set in setup_logging()
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8",
        },
    },
    "root": {"level": None, "handlers": ["console", "info_file_handler"]},  # set in setup_logging()
}


def setup_logging(
    data_dir_path,
    log_level,
):
    """
    Setup the logging configuration
    :param data_dir_path: data directory file path
    :param log_level: level to log from
    :return:
    """

    logger_configuration = deepcopy(LOGGER_CONFIG_DICT)
    _expanduser_log_file_paths(logger_configuration)
    logger_configuration["root"]["level"] = log_level
    logger_configuration["handlers"]["info_file_handler"]["filename"] = os.path.join(
        data_dir_path, "monkey_island.log"
    )
    logging.config.dictConfig(logger_configuration)


def _expanduser_log_file_paths(config: Dict):
    handlers = config.get("handlers", {})

    for handler_settings in handlers.values():
        if "filename" in handler_settings:
            handler_settings["filename"] = os.path.expanduser(handler_settings["filename"])
