from dataclasses import dataclass


@dataclass
class IslandArgs:
    setup_only: bool
    server_config: str


def parse_cli_args() -> IslandArgs:
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

    return IslandArgs(args.setup_only, args.server_config)
