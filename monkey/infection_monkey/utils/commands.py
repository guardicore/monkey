from infection_monkey.config import GUID
from infection_monkey.exploit.tools.helpers import AGENT_BINARY_PATH_LINUX, AGENT_BINARY_PATH_WIN64
from infection_monkey.model import CMD_CARRY_OUT, CMD_EXE, MONKEY_ARG
from infection_monkey.model.host import VictimHost

# Dropper target paths
DROPPER_TARGET_PATH_LINUX = AGENT_BINARY_PATH_LINUX
DROPPER_TARGET_PATH_WIN64 = AGENT_BINARY_PATH_WIN64


def build_monkey_commandline(target_host: VictimHost, depth: int, location: str = None) -> str:

    return " " + " ".join(
        build_monkey_commandline_explicitly(
            GUID,
            target_host.default_server,
            depth,
            location,
        )
    )


def build_monkey_commandline_explicitly(
    parent: str = None,
    server: str = None,
    depth: int = None,
    location: str = None,
) -> list:
    cmdline = []

    if parent is not None:
        cmdline.append("-p")
        cmdline.append(str(parent))
    if server is not None:
        cmdline.append("-s")
        cmdline.append(str(server))
    if depth is not None:
        cmdline.append("-d")
        cmdline.append(str(depth))
    if location is not None:
        cmdline.append("-l")
        cmdline.append(str(location))

    return cmdline


def get_monkey_commandline_windows(destination_path: str, monkey_cmd_args: list) -> list:
    monkey_cmdline = [CMD_EXE, CMD_CARRY_OUT, destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args


def get_monkey_commandline_linux(destination_path: str, monkey_cmd_args: list) -> list:
    monkey_cmdline = [destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args
