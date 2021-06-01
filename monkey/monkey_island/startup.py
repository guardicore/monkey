# This import patches other imports and needs to be first
import monkey_island.setup.gevent_setup  # noqa: F401 isort:skip

import json

from monkey_island.cc.arg_parser import parse_cli_args
from monkey_island.cc.server_setup import setup_island
from monkey_island.cc.server_utils.island_logger import setup_logging
from monkey_island.setup.config_setup import setup_config_by_cmd_arg, setup_default_config


def start_island():
    island_args = parse_cli_args()

    # This is here in order to catch EVERYTHING, some functions are being called on
    # imports, so the log init needs to be first.
    try:
        if island_args.server_config_path:
            config, server_config_path = setup_config_by_cmd_arg(island_args.server_config_path)
        else:
            config, server_config_path = setup_default_config()

        setup_logging(config.data_dir, config.log_level)

    except OSError as ex:
        print(f"Error opening server config file: {ex}")
        exit(1)

    except json.JSONDecodeError as ex:
        print(f"Error loading server config: {ex}")
        exit(1)

    setup_island(island_args.setup_only, config, server_config_path)


if "__main__" == __name__:
    start_island()
