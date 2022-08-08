import abc
from typing import Iterable

from common.credentials import Credentials
from infection_monkey.custom_types import PropagationCredentials


class IPropagationCredentialsRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_credentials(self, credentials_to_add: Iterable[Credentials]):
        """
        Adds credentials to the CredentialStore
        :param Iterable[Credentials] credentials_to_add: The credentials that will be added
        """

    @abc.abstractmethod
    def get_credentials(self) -> PropagationCredentials:
        """
        Retrieves credentials from the store
        :return: Credentials that can be used for propagation
        :type: PropagationCredentials
        """
