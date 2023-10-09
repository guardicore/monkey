from abc import ABC, abstractmethod
from typing import Sequence

from monkeytypes import Credentials


class ICredentialsRepository(ABC):
    """
    Store credentials that can be used to propagate around the network.

    This repository stores credentials that were either "configured" or "stolen". "Configured"
    credentials are provided to the simulation as input. "Stolen" credentials are collected during
    a simulation.
    """

    @abstractmethod
    def get_configured_credentials(self) -> Sequence[Credentials]:
        """
        Retrieve credentials that were configured.

        :raises RetrievalError: If an error is encountered while attempting to retrieve the
                                credentials
        :return: Sequence of configured credentials
        """

    @abstractmethod
    def get_stolen_credentials(self) -> Sequence[Credentials]:
        """
        Retrieve credentials that were stolen during a simulation.

        :raises RetrievalError: If an error is encountered while attempting to retrieve the
                                credentials
        :return: Sequence of stolen credentials
        """

    @abstractmethod
    def get_all_credentials(self) -> Sequence[Credentials]:
        """
        Retrieve all credentials in the repository.

        :raises RetrievalError: If an error is encountered while attempting to retrieve the
                                credentials
        :return: Sequence of stolen and configured credentials
        """

    @abstractmethod
    def save_configured_credentials(self, credentials: Sequence[Credentials]):
        """
        Save credentials that were configured.

        :param credentials: Configured Credentials to store in the repository
        :raises StorageError: If an error is encountered while attempting to store the credentials
        """

    @abstractmethod
    def save_stolen_credentials(self, credentials: Sequence[Credentials]):
        """
        Save credentials that were stolen during a simulation.

        :param credentials: Stolen Credentials to store in the repository
        :raises StorageError: If an error is encountered while attempting to store the credentials
        """

    @abstractmethod
    def remove_configured_credentials(self):
        """
        Remove credentials that were configured from the repository.

        :raises RemovalError: If an error is encountered while attempting to remove the credentials
        """

    @abstractmethod
    def remove_stolen_credentials(self):
        """
        Remove stolen credentials from the repository.

        :raises RemovalError: If an error is encountered while attempting to remove the credentials
        """

    @abstractmethod
    def remove_all_credentials(self):
        """
        Remove all credentials in the repository.

        :raises RemovalError: If an error is encountered while attempting to remove the credentials
        """

    @abstractmethod
    def reset(self):
        """
        An alias for remove_all_credentials()

        :raises RemovalError: If an error is encountered while attempting to remove the credentials
        """
