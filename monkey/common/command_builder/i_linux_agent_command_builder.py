import abc
from enum import Enum, auto
from pathlib import PurePosixPath
from typing import Optional

from monkeytypes import InfectionMonkeyBaseModel

from .environment import DropperExecutionMode


class LinuxDownloadMethod(Enum):
    WGET = auto()
    CURL = auto()


class LinuxDownloadOptions(InfectionMonkeyBaseModel):
    agent_destination_path: PurePosixPath
    download_method: LinuxDownloadMethod
    download_url: str


class LinuxRunOptions(InfectionMonkeyBaseModel):
    agent_destination_path: PurePosixPath
    dropper_execution_mode: DropperExecutionMode
    dropper_destination_path: Optional[PurePosixPath] = None

    # TODO: Validation rule that
    # If dropper_destination_path is None then DropperExecutionMode must be DROPPER


class ILinuxAgentCommandBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build_download_command(self, download_options: LinuxDownloadOptions):
        """
        Builds the download command for the Agent

        :param download_options: Options needed for the command to be built
        """

    @abc.abstractmethod
    def build_run_command(self, run_options: LinuxRunOptions):
        """
        Builds the run command for the Agent

        :param run_options: Options needed for the command to be built
        """

    @abc.abstractmethod
    def get_command(self) -> str:
        """
        Gets the resulting command
        """

    @abc.abstractclassmethod
    def reset_command(self):
        """
        Resets the command to empty one.
        """
