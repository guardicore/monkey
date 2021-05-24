from gevent import monkey as gevent_monkey

from monkey_island.cc.arg_parser import parse_cli_args
from monkey_island.setup.config_setup import setup_config_by_cmd_arg, setup_default_config

gevent_monkey.patch_all()

import json  # noqa: E402

from monkey_island.cc.server_utils.island_logger import setup_logging  # noqa: E402

if "__main__" == __name__:
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

    from monkey_island.cc.main import main  # noqa: E402

    main(island_args.setup_only, server_config_path, config)
