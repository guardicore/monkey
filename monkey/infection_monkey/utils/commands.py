from typing import List, Optional

from infection_monkey.config import GUID
from infection_monkey.exploit.tools.helpers import AGENT_BINARY_PATH_LINUX, AGENT_BINARY_PATH_WIN64
from infection_monkey.model import CMD_CARRY_OUT, CMD_EXE, MONKEY_ARG

# Dropper target paths
DROPPER_TARGET_PATH_LINUX = AGENT_BINARY_PATH_LINUX
DROPPER_TARGET_PATH_WIN64 = AGENT_BINARY_PATH_WIN64


def build_monkey_commandline(servers: List[str], depth: int, location: Optional[str] = None) -> str:

    return " " + " ".join(
        build_monkey_commandline_explicitly(
            GUID,
            servers,
            depth,
            location,
        )
    )


def build_monkey_commandline_explicitly(
    parent: Optional[str] = None,
    servers: Optional[List[str]] = None,
    depth: Optional[int] = None,
    location: Optional[str] = None,
) -> List[str]:
    cmdline = []

    if parent is not None:
        cmdline.append("-p")
        cmdline.append(str(parent))
    if servers:
        cmdline.append("-s")
        cmdline.append(",".join(servers))
    if depth is not None:
        cmdline.append("-d")
        cmdline.append(str(depth))
    if location is not None:
        cmdline.append("-l")
        cmdline.append(str(location))

    return cmdline


def get_monkey_commandline_windows(destination_path: str, monkey_cmd_args: List[str]) -> List[str]:
    monkey_cmdline = [CMD_EXE, CMD_CARRY_OUT, destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args


def get_monkey_commandline_linux(destination_path: str, monkey_cmd_args: List[str]) -> List[str]:
    monkey_cmdline = [destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args
