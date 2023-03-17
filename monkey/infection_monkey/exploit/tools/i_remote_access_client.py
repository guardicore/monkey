from abc import ABC, abstractmethod

from common.credentials import Credentials


class RemoteAuthenticationError(Exception):
    """Raised when authentication fails"""

    pass


class RemoteFileCopyError(Exception):
    """Raised when a remote file copy operation fails"""

    pass


class RemoteCommandExecutionError(Exception):
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
    def copy_file(self, file: bytes, dest: str):
        """
        :param file: File to copy
        :param dest: Destination path
        :raises RemoteFileCopyError: If copy failed
        """
        pass

    @abstractmethod
    def get_writable_paths(self) -> list[str]:
        """
        :return: List of available paths into which files can be copied
        """
        pass

    @abstractmethod
    def execute(self, command: str):
        """
        :param command: Command to execute
        :raises RemoteCommandExecutionError: If execution failed
        """
        pass
