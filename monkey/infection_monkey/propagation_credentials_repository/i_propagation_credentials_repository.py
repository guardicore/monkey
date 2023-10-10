import abc
from typing import Iterable

from monkeytypes import Credentials


class IPropagationCredentialsRepository(metaclass=abc.ABCMeta):
    """
    Repository that stores and provides credentials for the Agent to use in propagation
    """

    @abc.abstractmethod
    def add_credentials(self, credentials_to_add: Iterable[Credentials]):
        """
        Adds credentials to the CredentialStore
        :param credentials_to_add: The credentials that will be added
        """

    @abc.abstractmethod
    def get_credentials(self) -> Iterable[Credentials]:
        """
        Retrieves credentials from the store
        :return: Credentials that can be used for propagation
        """
