import json
import os
from pathlib import Path

from monkey_island.cc.server_utils.consts import (
    DEFAULT_DATA_DIR,
    DEFAULT_DEVELOP_SERVER_CONFIG_PATH,
    DEFAULT_LOG_LEVEL,
    DEFAULT_SERVER_CONFIG_PATH,
)


def create_default_server_config_file() -> None:
    if not os.path.isfile(DEFAULT_SERVER_CONFIG_PATH):
        write_default_server_config_to_file(DEFAULT_SERVER_CONFIG_PATH)


def write_default_server_config_to_file(path: str) -> None:
    default_config = Path(DEFAULT_DEVELOP_SERVER_CONFIG_PATH).read_text()
    Path(path).write_text(default_config)


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
