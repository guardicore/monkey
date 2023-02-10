import abc
from typing import BinaryIO


class IAgentBinaryRepository(metaclass=abc.ABCMeta):
    """
    A repository that retrieves the agent binaries
    """

    @abc.abstractmethod
    def get_linux_binary(self) -> BinaryIO:
        """
        Retrieve linux agent binary

        :return: A file-like object that represents the linux agent binary
        :raises RetrievalError: If the agent binary could not be retrieved
        """

    @abc.abstractmethod
    def get_windows_binary(self) -> BinaryIO:
        """
        Retrieve windows agent binary

        :return: A file-like object that represents the windows agent binary
        :raises RetrievalError: If the agent binary could not be retrieved
        """
