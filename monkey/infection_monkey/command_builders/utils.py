from pathlib import PurePath
from typing import Optional, Union

from agentpluginapi import DropperExecutionMode, LinuxRunOptions, WindowsRunOptions

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
