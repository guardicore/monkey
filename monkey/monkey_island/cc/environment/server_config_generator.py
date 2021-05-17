import os
from pathlib import Path

from monkey_island.cc.environment.data_dir_generator import create_default_data_dir
from monkey_island.cc.server_utils.consts import (
    DEFAULT_DEVELOP_SERVER_CONFIG_PATH,
    DEFAULT_SERVER_CONFIG_PATH,
)


def create_default_server_config_file() -> str:
    if not os.path.isfile(DEFAULT_SERVER_CONFIG_PATH):
        create_default_data_dir()
        write_default_server_config_to_file(DEFAULT_SERVER_CONFIG_PATH)
    return DEFAULT_SERVER_CONFIG_PATH


def write_default_server_config_to_file(path: str) -> None:
    default_config = Path(DEFAULT_DEVELOP_SERVER_CONFIG_PATH).read_text()
    Path(path).write_text(default_config)
