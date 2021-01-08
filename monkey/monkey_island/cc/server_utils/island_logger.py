import json
import logging.config
import os

__author__ = 'Maor.Rayzin'


def json_setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup the logging configuration
    :param default_path: the default log configuration file path
    :param default_level: Default level to log from
    :param env_key: SYS ENV key to use for external configuration file path
    :return:
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
