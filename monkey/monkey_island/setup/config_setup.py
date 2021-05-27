import os
from typing import Tuple

from monkey_island.cc.environment import server_config_handler
from monkey_island.cc.environment.utils import create_secure_directory
from monkey_island.cc.server_utils.consts import DEFAULT_DATA_DIR, DEFAULT_SERVER_CONFIG_PATH
from monkey_island.setup.island_config_options import IslandConfigOptions


def setup_config_by_cmd_arg(server_config_path) -> Tuple[IslandConfigOptions, str]:
    server_config_path = os.path.expandvars(os.path.expanduser(server_config_path))
    config = server_config_handler.load_server_config_from_file(server_config_path)
    create_secure_directory(config.data_dir, create_parent_dirs=True)
    return config, server_config_path


def setup_default_config() -> Tuple[IslandConfigOptions, str]:
    server_config_path = DEFAULT_SERVER_CONFIG_PATH
    create_secure_directory(DEFAULT_DATA_DIR, create_parent_dirs=False)
    server_config_handler.create_default_server_config_file()
    config = server_config_handler.load_server_config_from_file(server_config_path)
    return config, server_config_path
