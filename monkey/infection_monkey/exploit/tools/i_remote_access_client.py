from abc import ABC, abstractmethod

from common.credentials import Credentials


class RemoteAuthenticationError(Exception):
    pass


class RemoteFileCopyError(Exception):
    pass


class RemoteCommandExecutionError(Exception):
    pass


class IRemoteAccessClient(ABC):
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
    def get_available_paths(self) -> list[str]:
        """
        :return: List of available paths
        """
        pass

    @abstractmethod
    def execute(self, command: str):
        """
        :param command: Command to execute
        :raises RemoteCommandExecutionError: If execution failed
        """
        pass
