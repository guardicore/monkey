import os
from typing import Tuple

from monkey_island.cc.environment import server_config_handler
from monkey_island.cc.environment.data_dir_generator import create_data_dir  # noqa: E402
from monkey_island.cc.server_utils.consts import DEFAULT_DATA_DIR, DEFAULT_SERVER_CONFIG_PATH


def setup_config_by_cmd_arg(server_config_path) -> Tuple[dict, str]:
    server_config_path = os.path.expandvars(os.path.expanduser(server_config_path))
    config = server_config_handler.load_server_config_from_file(server_config_path)
    create_data_dir(config["data_dir"], create_parent_dirs=True)
    return config, server_config_path


def setup_default_config() -> Tuple[dict, str]:
    server_config_path = DEFAULT_SERVER_CONFIG_PATH
    create_data_dir(DEFAULT_DATA_DIR, create_parent_dirs=False)
    server_config_handler.create_default_server_config_file()
    config = server_config_handler.load_server_config_from_file(server_config_path)
    return config, server_config_path
