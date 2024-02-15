from pathlib import PurePath
from typing import Optional, Sequence, Union

from agentpluginapi import DropperExecutionMode, LinuxRunOptions, WindowsRunOptions
from monkeytypes import AgentID

from infection_monkey.model import DROPPER_ARG, MONKEY_ARG


def get_agent_argument(run_options: Union[WindowsRunOptions, LinuxRunOptions]) -> str:
    agent_arg = MONKEY_ARG
    if run_options.dropper_execution_mode == DropperExecutionMode.DROPPER:
        agent_arg = DROPPER_ARG

    return agent_arg


def get_agent_location(
    run_options: Union[WindowsRunOptions, LinuxRunOptions]
) -> Optional[PurePath]:
    destination_path = None
    if run_options.dropper_execution_mode == DropperExecutionMode.DROPPER:
        destination_path = (
            run_options.dropper_destination_path
            if run_options.dropper_destination_path
            else run_options.agent_destination_path
        )
    return destination_path


def build_monkey_commandline_parameters(
    parent: Optional[AgentID] = None,
    servers: Optional[Sequence[str]] = None,
    depth: Optional[int] = None,
    location: Union[str, PurePath, None] = None,
) -> Sequence[str]:
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
