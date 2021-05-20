from gevent import monkey as gevent_monkey

from monkey_island.cc.arg_parser import parse_cli_args
from monkey_island.config_file_parser import load_server_config_from_file
from monkey_island.setup.setup_param_factory import SetupParamFactory

gevent_monkey.patch_all()

import json  # noqa: E402

from monkey_island.cc.server_utils.island_logger import setup_logging  # noqa: E402

if "__main__" == __name__:
    island_args = parse_cli_args()
    config_contents = load_server_config_from_file(island_args.server_config_path)

    setup_params = SetupParamFactory().build(island_args, config_contents)

    try:

        # This is here in order to catch EVERYTHING, some functions are being called on
        # imports, so the log init needs to be first.
        setup_logging(setup_params.data_dir, setup_params.log_level)

    except OSError as ex:
        print(f"Error opening server config file: {ex}")
        exit(1)

    except json.JSONDecodeError as ex:
        print(f"Error loading server config: {ex}")
        exit(1)

    from monkey_island.cc.main import main  # noqa: E402

    main(setup_params)
