from monkey_island.cc.arg_parser import IslandCmdArgs
from monkey_island.cc.environment import server_config_handler
from monkey_island.cc.setup.island_config_options import IslandConfigOptions


def setup_default_config(
    island_args: IslandCmdArgs, data_dir_path: str
) -> [IslandConfigOptions, str]:
    if island_args.server_config_path:
        config = server_config_handler.load_server_config_from_file(data_dir_path)
        return config, island_args.server_config_path
    else:
        server_config_path = server_config_handler.create_default_server_config_file(data_dir_path)
        config = server_config_handler.load_server_config_from_file(server_config_path)
        return config, server_config_path
