from pathlib import PurePath
from typing import Optional, Union

from monkeytypes import AgentID

from infection_monkey.model import CMD_CARRY_OUT, CMD_EXE, MONKEY_ARG


def build_monkey_commandline_parameters(
    parent: Optional[AgentID] = None,
    servers: Optional[list[str]] = None,
    depth: Optional[int] = None,
    location: Union[str, PurePath, None] = None,
) -> list[str]:
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


def get_monkey_commandline_windows(destination_path: str, monkey_cmd_args: list[str]) -> list[str]:
    monkey_cmdline = [CMD_EXE, CMD_CARRY_OUT, destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args


def get_monkey_commandline_linux(destination_path: str, monkey_cmd_args: list[str]) -> list[str]:
    monkey_cmdline = [destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args
