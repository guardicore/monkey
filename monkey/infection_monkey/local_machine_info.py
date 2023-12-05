from pathlib import Path
from typing import Optional

from monkeytypes import MutableInfectionMonkeyBaseModel, OperatingSystem
from pydantic import Field

from common.utils.environment import get_os
from infection_monkey.utils.monkey_dir import get_monkey_dir_path


class LocalMachineInfo(MutableInfectionMonkeyBaseModel):
    """
    Contains information about the local machine

    :param operating_system: Operating system of the local machine
    :param temporary_directory: Path to a temporary directory on the local machine
                                to store artifacts
    :param interface_to_target: Interface on the local machine that can be reached
                                by the target machine
    """

    operating_system: OperatingSystem = Field(default_factory=get_os)
    temporary_directory: Path = Field(default_factory=get_monkey_dir_path)
    interface_to_target: Optional[str] = None

    def set_interface_to_target(self, interface_to_target: str):
        self.interface_to_target = interface_to_target

    def reset_interface_to_target(self):
        self.interface_to_target = None
