import abc
from typing import BinaryIO

from monkeytypes import OperatingSystem


class IAgentBinaryRepository(metaclass=abc.ABCMeta):
    """
    A repository that retrieves the agent binaries
    """

    @abc.abstractmethod
    def get_agent_binary(self, operating_system: OperatingSystem) -> BinaryIO:
        """
        Retrieve an agent binary for the specified operating system

        :param operating_system: The operating system with which the binary must be compatible
        :return: A file-like object that represents the agent binary
        :raises RetrievalError: If the agent binary could not be retrieved
        """
