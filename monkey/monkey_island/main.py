# This import patches other imports and needs to be first
import monkey_island.setup.gevent_setup  # noqa: F401 isort:skip

import sys

from monkey_island.cc.server_utils.island_logger import setup_default_failsafe_logging


def main():
    # This is here in order to catch EVERYTHING, some functions are being called on
    # imports, so the log init needs to be first.
    try:
        setup_default_failsafe_logging()
    except Exception as ex:
        print(f"Error configuring logging: {ex}")
        sys.exit(1)

    from monkey_island.cc.server_setup import run_monkey_island  # noqa: E402

    run_monkey_island()


if "__main__" == __name__:
    main()
