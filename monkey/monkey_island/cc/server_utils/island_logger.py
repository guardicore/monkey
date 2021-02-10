import json
import logging.config
import os
from typing import Dict

from monkey_island.cc.consts import DEFAULT_LOGGING_CONFIG_PATH

__author__ = "Maor.Rayzin"


def json_setup_logging(
    default_path=DEFAULT_LOGGING_CONFIG_PATH,
    default_level=logging.INFO,
    env_key="LOG_CFG",
):
    """
    Setup the logging configuration
    :param default_path: the default log configuration file path
    :param default_level: Default level to log from
    :param env_key: SYS ENV key to use for external configuration file path
    :return:
    """
    path = os.path.expanduser(default_path)
    value = os.getenv(env_key, None)

    if value:
        path = value

    if os.path.exists(path):
        with open(path, "rt") as f:
            config = json.load(f)
            _expanduser_log_file_paths(config)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def _expanduser_log_file_paths(config: Dict):
    handlers = config.get("handlers", {})

    for handler_settings in handlers.values():
        if "filename" in handler_settings:
            handler_settings["filename"] = os.path.expanduser(
                handler_settings["filename"]
            )
