from monkey_island.cc.server_utils.consts import (
    DEFAULT_SERVER_CONFIG_PATH,
    DEFAULT_SHOULD_SETUP_ONLY,
)


class IslandCmdArgs:
    setup_only: bool = DEFAULT_SHOULD_SETUP_ONLY
    server_config_path: str = DEFAULT_SERVER_CONFIG_PATH

    def __init__(self, setup_only: None, server_config_path: None):
        if setup_only:
            self.setup_only = setup_only
        if server_config_path:
            self.server_config_path = server_config_path


def parse_cli_args() -> IslandCmdArgs:
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
        "--server-config", action="store", help="The path to the server configuration file."
    )
    args = parser.parse_args()

    return IslandCmdArgs(args.setup_only, args.server_config)
