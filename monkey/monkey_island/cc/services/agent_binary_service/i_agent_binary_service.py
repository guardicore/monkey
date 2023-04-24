import abc
from typing import BinaryIO


class IAgentBinaryService(metaclass=abc.ABCMeta):
    """
    A service for retrieving and manipulating agent binaries
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
