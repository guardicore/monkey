import abc
from typing import Iterable

from infection_monkey.i_puppet import Credentials
from infection_monkey.typing import PropagationCredentials


class ICredentialsStore(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_credentials(self, credentials_to_add: Iterable[Credentials]):
        """
        Adds credentials to the CredentialStore
        :param Iterable[Credentials] credentials: The credentials that will be added
        """

    @abc.abstractmethod
    def get_credentials(self) -> PropagationCredentials:
        """
        Retrieves credentials from the store
        :return: Credentials that can be used for propagation
        :type: PropagationCredentials
        """
