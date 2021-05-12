import json
import os

import monkey_island.cc.environment.server_config_generator as server_config_generator
from monkey_island.cc.server_utils.consts import DEFAULT_DATA_DIR, DEFAULT_SERVER_CONFIG_PATH

DEFAULT_LOG_LEVEL = "INFO"


def create_default_server_config_path():
    if not os.path.isfile(DEFAULT_SERVER_CONFIG_PATH):
        if not os.path.isdir(DEFAULT_DATA_DIR):
            os.mkdir(DEFAULT_DATA_DIR, mode=0o700)
        server_config_generator.create_default_config_file(DEFAULT_SERVER_CONFIG_PATH)
    return DEFAULT_SERVER_CONFIG_PATH


def load_server_config_from_file(server_config_path):
    with open(server_config_path, "r") as f:
        config_content = f.read()
        config = json.loads(config_content)
        add_default_values_to_config(config)

        return config


def add_default_values_to_config(config):
    config["data_dir"] = os.path.abspath(
        os.path.expanduser(os.path.expandvars(config.get("data_dir", DEFAULT_DATA_DIR)))
    )

    config.setdefault("log_level", DEFAULT_LOG_LEVEL)

    return config
