from abc import ABC, abstractmethod
from pathlib import PurePath
from typing import Collection

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
        Establish an authenticated session with the remote host

        :param credentials: Credentials to use for login
        :raises RemoteAuthenticationError: If login failed
        """
        pass

    @abstractmethod
    def get_os(self) -> OperatingSystem:
        """
        Query the remote host for its operating system

        :return: The operating system of the remote host
        :raises RemoteAccessClientError: If the operating system could not be determined
        """
        pass

    @abstractmethod
    def copy_file(self, file: bytes, dest: PurePath):
        """
        Copy a file to the remote host

        :param file: File to copy
        :param dest: Destination path
        :raises RemoteFileCopyError: If copy failed
        """
        pass

    @abstractmethod
    def get_writable_paths(self) -> Collection[PurePath]:
        """
        Query the remote host and return a collection of writable paths

        :return: List of available paths into which files can be copied
        """
        pass

    @abstractmethod
    def execute_detached(self, command: str):
        """
        Execute a command on the remote host in a detached process

        The command will be executed in a detached process, which allows the client to disconnect
        from the remote host while allowing the command to continue running.

        :param command: Command to execute
        :raises RemoteCommandExecutionError: If execution failed
        """
        pass
