from abc import ABC
from typing import Sequence

from monkey_island.cc.services.telemetry.processing.credentials import Credentials


class ICredentialsRepository(ABC):
    def get_configured_credentials(self) -> Sequence[Credentials]:
        """
        Retrieve all credentials that were configured.

        :raises RetrievalError: If an error is encountered while attempting to retrieve configured
                                credentials
        :return: Sequence of configured credentials
        """
        pass

    def save_configured_credentials(self, credentials: Credentials):
        """
        Save credentials which are configured.

        :param credentials: Credentials that are going to be stored
        :raises StorageError: If an error is encountered while attempting to store configured
                              credentials
        """
        pass

    def remove_configured_credentials(self):
        """
        Remove all configured credentials.

        :raises RemovalError: If an error is encountered while attempting to remove configured
                              credentials
        """
        pass

    def get_stolen_credentials(self) -> Sequence[Credentials]:
        """
        Retrieve credentials that are stolen

        :raises RetrievalError: If an error is encountered while attempting to retrieve stolen
                                credentials
        :return: Sequence of all stolen credentials
        """
        pass

    def save_stolen_credentials(self, credentials: Credentials):
        """
        Save credentials which are stolen.

        :param credentials: Credentials that are going to be stored
        :raises StorageError: If an error is encountered while attempting to store stolen
                              credentials
        """
        pass

    def remove_stolen_credentials(self):
        """
        Remove all credentials from the repository.

        :raises RemovalError: If an error is encountered while attempting to remove the credentials
        """
        pass

    def get_all_credentials(self) -> Sequence[Credentials]:
        """
        Retrieve stolen and configured credentials.

        :raises RetrievalError: If an error is encountered while attempting to retrieve the
                                credentials
        :return: Sequence of stolen and configured credentials
        """
        pass

    def remove_all_credentials(self):
        """
        Remove all the credentials in the repository.

        :raises RemovalError: If an error is encountered while attempting to remove the credentials
        """
        pass
