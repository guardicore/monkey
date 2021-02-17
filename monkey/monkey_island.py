from gevent import monkey as gevent_monkey

gevent_monkey.patch_all()

from monkey_island.cc.main import main  # noqa: E402
from monkey_island.cc.environment.environment_config import DEFAULT_SERVER_CONFIG_PATH  # noqa: E402


def parse_cli_args():
    import argparse
    parser = argparse.ArgumentParser(description="Infection Monkey Island CnC Server.  See https://infectionmonkey.com",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--setup-only", action="store_true",
                        help="Pass this flag to cause the Island to setup and exit without actually starting. "
                             "This is useful for preparing Island to boot faster later-on, so for "
                             "compiling/packaging Islands.")
    parser.add_argument("-c", "--config", action="store",
                        help="The path to the server configuration file.",
                        default=DEFAULT_SERVER_CONFIG_PATH)
    args = parser.parse_args()
    return (args.setup_only, args.config)


if "__main__" == __name__:
    (is_setup_only, config) = parse_cli_args()
    main(is_setup_only, config)
