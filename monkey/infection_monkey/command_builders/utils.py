from pathlib import PurePath
from typing import Optional, Sequence, Union

from agentpluginapi import DropperExecutionMode, LinuxRunOptions, WindowsRunOptions
from monkeytypes import AgentID

from infection_monkey.model import DROPPER_ARG, MONKEY_ARG


def get_agent_argument(run_options: Union[WindowsRunOptions, LinuxRunOptions]) -> str:
    """
    Get the appropriate agent argument based on the run options.

    :param run_options: The run command options.
    :raises ValueError: If dropper execution mode is not DROPPER or NONE.
    :return: The Agent argument to be used.
    """
    agent_arg = MONKEY_ARG
    if run_options.dropper_execution_mode == DropperExecutionMode.DROPPER:
        agent_arg = DROPPER_ARG
    if run_options.dropper_execution_mode not in [
        DropperExecutionMode.DROPPER,
        DropperExecutionMode.NONE,
    ]:
        raise ValueError(
            "Agent argument can only be used with"
            "DropperExecutionMode.DROPPER or DropperExecutionMode.NONE."
        )

    return agent_arg


def get_agent_location(
    run_options: Union[WindowsRunOptions, LinuxRunOptions]
) -> Optional[PurePath]:
    """
    Get the agent location based on the run options.

    :param run_options: The run command options.
    :return: The destination path for the agent, or None if not applicable.
    """
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
    """
    Build command-line parameters for the Agent.

    :param parent: The ID of the parent Agent, if applicable.
    :param servers: A sequence of server addresses.
    :param depth: The depth of which the Agent will run upon.
    :param location: The location of the Dropper on the victim machine.
    :return: A sequence of command-line parameters.
    """
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
