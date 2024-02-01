import abc
from enum import Enum, auto
from pathlib import PurePath
from typing import Optional

from monkeytypes import InfectionMonkeyBaseModel


class DownloadMethod(Enum):
    WGET = auto()
    CURL = auto()
    WEB_REQUEST = auto()
    WEB_CLIENT = auto()


class Shell(Enum):
    BASH = auto()
    CMD = auto()
    POWERSHELL = auto()


class MonkeyArgs(Enum):
    AGENT = auto()
    DROPPER = auto()


class AbstractCommandModel(InfectionMonkeyBaseModel):
    agent_destination_path: PurePath
    shell: Optional[Shell] = None
    prefix: Optional[str] = None


class DownloadOptions(AbstractCommandModel):
    download_method: DownloadMethod
    download_url: str


class RunOptions(AbstractCommandModel):
    monkey_args: Optional[MonkeyArgs]
    postfix: Optional[str] = None


class IAgentCommandBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build_download_command(self, download_options: DownloadOptions) -> str:
        """
        Builds the download command for the Agent

        :param download_options: Options needed for the command to be built
        """

    @abc.abstractmethod
    def build_run_command(self, run_options: RunOptions) -> str:
        """
        Builds the run command for the Agent

        :param run_options: Options needed for the command to be built
        """

    @abc.abstractmethod
    def build_agent_command_line_arguments(self, destination_path: Optional[PurePath]) -> list[str]:
        """
        Builds the run command for the Agent
        """
