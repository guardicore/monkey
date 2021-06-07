import os
from typing import Tuple

from monkey_island.cc.arg_parser import IslandCmdArgs
from monkey_island.cc.environment import server_config_handler
from monkey_island.cc.environment.utils import create_secure_directory
from monkey_island.cc.server_utils.consts import DEFAULT_SERVER_CONFIG_PATH
from monkey_island.cc.setup.island_config_options import IslandConfigOptions


def setup_data_dir(island_args: IslandCmdArgs) -> Tuple[IslandConfigOptions, str]:
    if island_args.server_config_path:
        return _setup_config_by_cmd_arg(island_args.server_config_path)

    return _setup_default_config()


def _setup_config_by_cmd_arg(server_config_path) -> Tuple[IslandConfigOptions, str]:
    server_config_path = os.path.expandvars(os.path.expanduser(server_config_path))
    config = server_config_handler.load_server_config_from_file(server_config_path)
    create_secure_directory(config.data_dir, create_parent_dirs=True)
    return config, server_config_path


def _setup_default_config() -> Tuple[IslandConfigOptions, str]:
    config = server_config_handler.load_server_config_from_file(DEFAULT_SERVER_CONFIG_PATH)
    create_secure_directory(config.data_dir, create_parent_dirs=False)
    server_config_path = server_config_handler.create_default_server_config_file(config.data_dir)
    return config, server_config_path
