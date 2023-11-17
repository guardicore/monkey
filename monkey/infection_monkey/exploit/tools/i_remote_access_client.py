from abc import ABC, abstractmethod
from pathlib import PurePath
from typing import Collection, Set

from monkeyevents import AgentEventTag
from monkeytypes import Credentials, OperatingSystem


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
    def login(self, credentials: Credentials, tags: Set[AgentEventTag]):
        """
        Establish an authenticated session with the remote host

        The `tags` argument will be updated with the techniques used to login.

        :param credentials: Credentials to use for login
        :param tags: Tags describing the techniques used to login
        :raises RemoteAuthenticationError: If login failed
        """
        pass

    @abstractmethod
    def get_os(self) -> OperatingSystem:
        """
        Return the operating system of the remote host

        :return: The operating system of the remote host
        :raises RemoteAccessClientError: If the operating system could not be determined
        """
        pass

    @abstractmethod
    def copy_file(self, file: bytes, dest: PurePath, tags: Set[AgentEventTag]):
        """
        Copy a file to the remote host

        The `tags` argument will be updated with the techniques used to copy the file.

        :param file: File to copy
        :param dest: Destination path
        :param tags: Tags describing the techniques used to copy the file
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
    def execute_agent(self, agent_binary_path: PurePath, tags: Set[AgentEventTag]):
        """
        Execute the agent on the remote host in a detached process

        The agent will be executed in a detached process, which allows the client to disconnect
        from the remote host while allowing the agent to continue running.

        The `tags` argument will be updated with the techniques used to execute the command.

        :param agent_binary_path: The path of the agent binary on the remote system
        :param tags: Tags describing the techniques used to execute the agent
        :raises RemoteCommandExecutionError: If execution failed
        """
        pass
