from gevent import monkey as gevent_monkey

from monkey_island.cc.arg_parser import parse_cli_args
from monkey_island.config_file_parser import load_island_config_from_file

gevent_monkey.patch_all()

import json  # noqa: E402

from monkey_island.cc.server_utils.island_logger import setup_logging  # noqa: E402

if "__main__" == __name__:
    island_args = parse_cli_args()

    try:
        # This is here in order to catch EVERYTHING, some functions are being called on
        # imports, so the log init needs to be first.
        config_options = load_island_config_from_file(island_args.server_config_path)
        setup_logging(config_options.data_dir, config_options.log_level)

    except OSError as ex:
        print(f"Error opening server config file: {ex}")
        exit(1)

    except json.JSONDecodeError as ex:
        print(f"Error loading server config: {ex}")
        exit(1)

    from monkey_island.cc.main import main  # noqa: E402

    main(island_args.setup_only, island_args.server_config_path, config_options)
