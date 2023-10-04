import abc
from typing import BinaryIO, Optional

from monkeytypes import OperatingSystem


class IAgentBinaryService(metaclass=abc.ABCMeta):
    """
    A service for retrieving and manipulating agent binaries
    """

    @abc.abstractmethod
    def get_agent_binary(self, operating_system: OperatingSystem) -> BinaryIO:
        """
        Retrieve an agent binary for the specified operating system

        :param operating_system: The operating system with which the binary must be compatible
        :return: A file-like object that represents the agent binary
        :raises RetrievalError: If the agent binary could not be retrieved
        """

    @abc.abstractmethod
    def get_masque(self, operating_system: OperatingSystem) -> Optional[bytes]:
        """
        Retrieve os specific agent binary masque

        :param operating_system: Operating system type
        :return: A bytes object that represent the masque
        """

    @abc.abstractmethod
    def set_masque(self, operating_system: OperatingSystem, masque: Optional[bytes]):
        """
        Set os-specific agent binary masque

        :param operating_system: Operating system type
        :param masque: The value to set the os-specific masque to
        """
