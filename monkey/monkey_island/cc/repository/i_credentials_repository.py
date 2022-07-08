from abc import ABC
from typing import Optional, Sequence

from common.credentials import Credentials


class ICredentialsRepository(ABC):
    """
    Store credentials that can be used to propagate around the network.

    This repository stores credentials that were either "configured" or "stolen". "Configured"
    credentials are provided to the simulation as input. "Stolen" credentials are collected during
    a simulation.
    """

    def get_credentials(
        self, origin: Optional[str], secret_type: Optional[str]
    ) -> Sequence[Credentials]:
        """
        Retrieve credentials in the repository.

        :param origin: String representing the origin of the credentials
        :param secret_type: String representing secret type
        :raises RetrievalError: If an error is encountered while attempting to retrieve the
                                credentials
        :return: Sequence of filtered credentials
        """
        pass

    def save_credentials(self, credentials: Credentials, origin: str):
        """
        Save credentials that were configured.

        :param origin: String representing the origin of credentials
        :param credentials: Configured Credentials to store in the repository
        :raises StorageError: If an error is encountered while attempting to store the credentials
        """
        pass

    def remove_credentials(self, origin: Optional[str]):
        """
        Remove all credentials in the repository.

        :param origin: String representing the origin of the credentials
        :raises RemovalError: If an error is encountered while attempting to remove the credentials
        """
        pass
