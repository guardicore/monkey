from pathlib import Path
from typing import Optional

from monkeytypes import MutableInfectionMonkeyBaseModel, OperatingSystem


class LocalMachineInfo(MutableInfectionMonkeyBaseModel):
    """
    Contains information about the local machine

    :param operating_system: Operating system of the local machine
    :param temporary_directory: Path to a temporary directory on the local machine
                                to store artifacts
    :param interface_to_target: Interface on the local machine that can be reached
                                by the target machine
    """

    operating_system: OperatingSystem
    temporary_directory: Path
    interface_to_target: Optional[str] = None

    def set_interface_to_target(self, interface_to_target: str):
        self.interface_to_target = interface_to_target

    def reset_interface_to_target(self):
        self.interface_to_target = None
