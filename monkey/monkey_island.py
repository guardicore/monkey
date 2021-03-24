from gevent import monkey as gevent_monkey

from monkey_island.cc.arg_parser import parse_cli_args

gevent_monkey.patch_all()

import json  # noqa: E402

from monkey_island.cc.island_logger import json_setup_logging  # noqa: E402


if "__main__" == __name__:
    island_args = parse_cli_args()

    # This is here in order to catch EVERYTHING, some functions are being called on
    # imports, so the log init needs to be first.
    try:
        json_setup_logging(island_args.logger_config)
    except json.JSONDecodeError as ex:
        print(f"Error loading logging config: {ex}")
        exit(1)

    from monkey_island.cc.main import main  # noqa: E402

    main(island_args.setup_only, island_args.server_config)
