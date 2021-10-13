from common.utils.file_utils import expand_path
from monkey_island.cc.arg_parser import IslandCmdArgs
from monkey_island.cc.environment import server_config_handler
from monkey_island.cc.server_utils.consts import DEFAULT_SERVER_CONFIG_PATH
from monkey_island.cc.server_utils.file_utils import create_secure_directory


def create_data_dir(island_args: IslandCmdArgs) -> str:
    if island_args.server_config_path:
        data_dir_path = _get_data_dir_path_from_args(island_args)
    else:
        data_dir_path = _get_data_dir_path_from_defaults()

    _create_data_dir(data_dir_path)
    return data_dir_path


def _get_data_dir_path_from_args(island_args: IslandCmdArgs) -> str:
    server_config_path = expand_path(island_args.server_config_path)
    config = server_config_handler.load_server_config_from_file(server_config_path)
    return str(config.data_dir)


def _get_data_dir_path_from_defaults() -> str:
    default_config = server_config_handler.load_server_config_from_file(DEFAULT_SERVER_CONFIG_PATH)
    return str(default_config.data_dir)


def _create_data_dir(path: str):
    create_secure_directory(path)
