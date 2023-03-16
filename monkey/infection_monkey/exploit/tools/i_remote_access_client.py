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
        :raises RemoteAuthenticationError: If login failed
        """
        pass

    @abstractmethod
    def copy_file(self, src: str, dest: str):
        """
        :raises RemoteFileCopyError: If copy failed
        """
        pass

    @abstractmethod
    def execute(self, command: str):
        """
        :raises RemoteCommandExecutionError: If execution failed
        """
        pass
