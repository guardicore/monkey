import json
import os
from pathlib import Path

from monkey_island.cc.server_utils.consts import DEFAULT_SERVER_CONFIG_PATH, SERVER_CONFIG_FILENAME
from monkey_island.cc.setup.island_config_options import IslandConfigOptions


def create_default_server_config_file(data_dir: str) -> str:
    config_file_path = os.path.join(data_dir, SERVER_CONFIG_FILENAME)
    if not os.path.isfile(config_file_path):
        write_default_server_config_to_file(config_file_path)

    return config_file_path


def write_default_server_config_to_file(path: str) -> None:
    default_config = Path(DEFAULT_SERVER_CONFIG_PATH).read_text()
    Path(path).write_text(default_config)


def load_server_config_from_file(server_config_path) -> IslandConfigOptions:
    with open(server_config_path, "r") as f:
        config_content = f.read()
        config = json.loads(config_content)

        return IslandConfigOptions(config)
