from abc import ABC, abstractmethod
from typing import Optional

from monkeytypes import OperatingSystem


class IMasqueradeRepository(ABC):
    """
    Store the masques that are to be applied to the Agent binaries.

    This repository stores the configured Linux and Windows masques.
    These masques are applied to the Agent binaries before propagation.
    """

    @abstractmethod
    def get_masque(self, operating_system: OperatingSystem) -> Optional[bytes]:
        """
        Retrieve the masque for the specified OS.

        :param operating_system: The OS whose masque is to be retrieved
        :return: The masque for the specified OS
        :raises RetrievalError: If an error is encountered while attempting to retrieve the
                                masque
        """

    @abstractmethod
    def set_masque(self, operating_system: OperatingSystem, masque: Optional[bytes]):
        """
        Set the masque for the specified OS.

        :param operating_system: The OS whose masque is to be set
        :param masque: The value to set the masque to, or None to clear the masque
        :raises StorageError: If an error is encountered while attempting to store the masque
        """

    @abstractmethod
    def reset(self):
        """
        Removes all masques in the repository

        :raises RemovalError: If an error is encountered while attempting to remove the masques
        """
