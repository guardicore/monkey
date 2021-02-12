from gevent import monkey as gevent_monkey

gevent_monkey.patch_all()

import json  # noqa: E402

from monkey_island.cc.consts import (
    DEFAULT_SERVER_CONFIG_PATH,
    DEFAULT_LOGGER_CONFIG_PATH,
)  # noqa: E402
from monkey_island.cc.island_logger import json_setup_logging  # noqa: E402


def parse_cli_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Infection Monkey Island CnC Server.  See https://infectionmonkey.com",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-s",
        "--setup-only",
        action="store_true",
        help="Pass this flag to cause the Island to setup and exit without actually starting. "
        "This is useful for preparing Island to boot faster later-on, so for "
        "compiling/packaging Islands.",
    )
    parser.add_argument(
        "--server-config",
        action="store",
        help="The path to the server configuration file.",
        default=DEFAULT_SERVER_CONFIG_PATH,
    )
    parser.add_argument(
        "--logger-config",
        action="store",
        help="The path to the logging configuration file.",
        default=DEFAULT_LOGGER_CONFIG_PATH,
    )
    args = parser.parse_args()

    return (args.setup_only, args.server_config, args.logger_config)


if "__main__" == __name__:
    # TODO: Address https://github.com/guardicore/monkey/pull/963#discussion_r575022748
    # before merging appimage PR
    (is_setup_only, server_config, logger_config) = parse_cli_args()

    # This is here in order to catch EVERYTHING, some functions are being called on
    # imports, so the log init needs to be first.
    try:
        json_setup_logging(logger_config)
    except (json.JSONDecodeError) as ex:
        print(f"Error loading logging config: {ex}")
        exit(1)

    from monkey_island.cc.main import main  # noqa: E402

    main(is_setup_only, server_config)
