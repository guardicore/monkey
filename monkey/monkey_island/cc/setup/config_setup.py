from typing import Tuple

from common.utils.file_utils import expand_path
from monkey_island.cc.arg_parser import IslandCmdArgs
from monkey_island.cc.environment import server_config_handler
from monkey_island.cc.server_utils.consts import DEFAULT_SERVER_CONFIG_PATH
from monkey_island.cc.setup.data_dir import setup_data_dir
from monkey_island.cc.setup.island_config_options import IslandConfigOptions


def setup_server_config(island_args: IslandCmdArgs) -> Tuple[IslandConfigOptions, str]:
    if island_args.server_config_path:
        return _setup_config_by_cmd_arg(island_args.server_config_path)

    return _setup_default_config()


def _setup_config_by_cmd_arg(server_config_path) -> Tuple[IslandConfigOptions, str]:
    server_config_path = expand_path(server_config_path)
    config = server_config_handler.load_server_config_from_file(server_config_path)

    # TODO refactor like in https://github.com/guardicore/monkey/pull/1528 because
    # there's absolutely no reason to be exposed to IslandConfigOptions extraction logic
    # if you want to modify data directory related code.
    setup_data_dir(str(config.data_dir))

    return config, server_config_path


def _setup_default_config() -> Tuple[IslandConfigOptions, str]:
    default_config = server_config_handler.load_server_config_from_file(DEFAULT_SERVER_CONFIG_PATH)
    default_data_dir = default_config.data_dir

    # TODO refactor like in https://github.com/guardicore/monkey/pull/1528 because
    # there's absolutely no reason to be exposed to IslandConfigOptions extraction logic
    # if you want to modify data directory related code.
    setup_data_dir(str(default_data_dir))

    server_config_path = server_config_handler.create_default_server_config_file(default_data_dir)
    config = server_config_handler.load_server_config_from_file(server_config_path)

    return config, server_config_path
