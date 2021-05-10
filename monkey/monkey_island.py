from gevent import monkey as gevent_monkey

from monkey_island.cc.arg_parser import parse_cli_args

gevent_monkey.patch_all()

import json  # noqa: E402
import os  # noqa: E402
from pathlib import Path  # noqa: E402

import monkey_island.cc.environment.server_config_generator as server_config_generator  # noqa: E402
from monkey_island.cc.server_utils.consts import DEFAULT_DATA_DIR, DEFAULT_LOG_LEVEL  # noqa: E402
from monkey_island.cc.server_utils.island_logger import json_setup_logging  # noqa: E402

if "__main__" == __name__:
    island_args = parse_cli_args()

    # This is here in order to catch EVERYTHING, some functions are being called on
    # imports, so the log init needs to be first.
    try:
        server_config_path = os.path.expanduser(island_args.server_config)
        if not Path(server_config_path).is_file():
            server_config_generator.create_default_config_file(server_config_path)

        with open(server_config_path, "r") as f:
            config_content = f.read()
        data = json.loads(config_content)
        data_dir = os.path.abspath(
            os.path.expanduser(
                os.path.expandvars(data["data_dir"] if "data_dir" in data else DEFAULT_DATA_DIR)
            )
        )
        log_level = data["log_level"] if "log_level" in data else DEFAULT_LOG_LEVEL

        # json_setup_logging(data_dir, log_level)

    except json.JSONDecodeError as ex:
        print(f"Error loading logging config: {ex}")
        exit(1)

    from monkey_island.cc.main import main  # noqa: E402

    main(island_args.setup_only, island_args.server_config)
