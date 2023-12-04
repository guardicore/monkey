from pathlib import Path
from typing import Optional

from monkeytypes import MutableInfectionMonkeyBaseModel, OperatingSystem
from pydantic import Field

from common.utils.environment import get_os


class LocalMachineInfo(MutableInfectionMonkeyBaseModel):
    operating_system: OperatingSystem = Field(default_factory=get_os)
    interface_to_target: Optional[str] = None
    temporary_directory: Optional[Path] = None

    def set_interface_to_target(self, interface_to_target: str):
        self.interface_to_target = interface_to_target

    def set_temporary_directory(self, temporary_directory: Path):
        self.temporary_directory = temporary_directory

    def reset_interface_to_target(self):
        self.interface_to_target = None

    def reset_temporary_directory(self):
        self.temporary_directory = None
