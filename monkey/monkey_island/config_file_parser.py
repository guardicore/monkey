import json
from os.path import isfile

from monkey_island.cc.server_utils.consts import DEFAULT_SERVER_CONFIG_PATH
from monkey_island.setup.island_config_options import IslandConfigOptions


def load_island_config_from_file(server_config_path: str) -> IslandConfigOptions:
    config_contents = read_config_file(server_config_path)
    return IslandConfigOptions.build_from_config_file_contents(config_contents)


def read_config_file(server_config_path: str) -> dict:
    if not server_config_path or not isfile(server_config_path):
        server_config_path = DEFAULT_SERVER_CONFIG_PATH
    with open(server_config_path, "r") as f:
        config_content = f.read()
        config = json.loads(config_content)
        return config
