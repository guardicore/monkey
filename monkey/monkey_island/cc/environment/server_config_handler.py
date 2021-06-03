import json
import os
from pathlib import Path

from monkey_island.cc.server_utils.consts import (
    DEFAULT_DEVELOP_SERVER_CONFIG_PATH,
    DEFAULT_SERVER_CONFIG_PATH,
)
from monkey_island.cc.setup.island_config_options import IslandConfigOptions


def create_default_server_config_file() -> None:
    if not os.path.isfile(DEFAULT_SERVER_CONFIG_PATH):
        write_default_server_config_to_file(DEFAULT_SERVER_CONFIG_PATH)


def write_default_server_config_to_file(path: str) -> None:
    default_config = Path(DEFAULT_DEVELOP_SERVER_CONFIG_PATH).read_text()
    Path(path).write_text(default_config)


def load_server_config_from_file(server_config_path) -> IslandConfigOptions:
    with open(server_config_path, "r") as f:
        config_content = f.read()
        config = json.loads(config_content)

        return IslandConfigOptions(config)
