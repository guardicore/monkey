from abc import ABC, abstractmethod
from pathlib import PurePath

from common import OperatingSystem
from common.credentials import Credentials


class RemoteAccessClientError(Exception):
    """Raised when the IRemoteAccessClient encounters an error"""

    pass


class RemoteAuthenticationError(RemoteAccessClientError):
    """Raised when authentication fails"""

    pass


class RemoteFileCopyError(RemoteAccessClientError):
    """Raised when a remote file copy operation fails"""

    pass


class RemoteCommandExecutionError(RemoteAccessClientError):
    """Raised when a remote command fails to execute"""

    pass


class IRemoteAccessClient(ABC):
    """An interface for clients that execute remote commands"""

    @abstractmethod
    def login(self, credentials: Credentials):
        """
        :param credentials: Credentials to use for login
        :raises RemoteAuthenticationError: If login failed
        """
        pass

    @abstractmethod
    def get_os(self) -> OperatingSystem:
        """
        Queries the remote host for the operating system and returns it

        :return: The operating system of the remote host
        :raises RemoteAccessClientError: If the operating system could not be determined
        """
        pass

    @abstractmethod
    def copy_file(self, file: bytes, dest: PurePath):
        """
        :param file: File to copy
        :param dest: Destination path
        :raises RemoteFileCopyError: If copy failed
        """
        pass

    @abstractmethod
    def get_writable_paths(self) -> list[PurePath]:
        """
        :return: List of available paths into which files can be copied
        """
        pass

    @abstractmethod
    def execute_detached(self, command: str):
        """
        Execute a command on the remote host

        This command will be executed in a detached process.

        :param command: Command to execute
        :raises RemoteCommandExecutionError: If execution failed
        """
        pass
