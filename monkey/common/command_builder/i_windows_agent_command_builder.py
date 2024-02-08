import abc
from enum import Enum, auto
from pathlib import PureWindowsPath
from typing import Optional

from monkeytypes import InfectionMonkeyBaseModel

from .environment import DropperExecutionMode

# from pydantic import model_validator


class WindowsDownloadMethod(Enum):
    WEB_REQUEST = auto()
    WEB_CLIENT = auto()


class WindowsShell(Enum):
    CMD = auto()
    POWERSHELL = auto()


class WindowsDownloadOptions(InfectionMonkeyBaseModel):
    agent_destination_path: PureWindowsPath
    download_method: WindowsDownloadMethod
    download_url: str


class WindowsRunOptions(InfectionMonkeyBaseModel):
    agent_destination_path: PureWindowsPath
    dropper_execution_mode: DropperExecutionMode
    shell: WindowsShell
    dropper_destination_path: Optional[PureWindowsPath] = None

    # TODO: Validation rule that
    # If dropper_destination_path is None then DropperExecutionMode must be DROPPER
    # @model_validator(mode='after')
    # def check_dropper_execution(self) -> 'WindowsDownloadOptions':
    #    if self.dropper_destination_path is None and self.dropper_execution_mode
    #    != DropperExecutionMode.DROPPER:
    #        raise ValueError('Dropper execution mode should be DropperExecutionMode.DROPPER
    #  if dropper_destination_path is None')
    #    return self


class IWindowsAgentCommandBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build_download_command(self, download_options: WindowsDownloadOptions):
        """
        Builds the download command for the Agent

        :param download_options: Options needed for the command to be built
        """

    @abc.abstractmethod
    def build_run_command(self, run_options: WindowsRunOptions):
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
