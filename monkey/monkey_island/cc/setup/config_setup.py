from common.utils.file_utils import expand_path
from monkey_island.cc.arg_parser import IslandCmdArgs
from monkey_island.cc.environment import server_config_handler
from monkey_island.cc.server_utils.consts import DEFAULT_SERVER_CONFIG_PATH
from monkey_island.cc.setup.island_config_options import IslandConfigOptions


def extract_server_config(island_args: IslandCmdArgs) -> IslandConfigOptions:
    if island_args.server_config_path:
        path_to_config = expand_path(island_args.server_config_path)
    else:
        path_to_config = DEFAULT_SERVER_CONFIG_PATH

    return server_config_handler.load_server_config_from_file(path_to_config)
