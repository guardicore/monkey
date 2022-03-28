import abc
from typing import Iterable, Mapping

from infection_monkey.i_puppet import Credentials


class ICredentialsStore(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_credentials(self, credentials_to_add: Iterable[Credentials]) -> None:
        """a
        Method that adds credentials to the CredentialStore
        :param Credentials credentials: The credentials that will be added
        """

    @abc.abstractmethod
    def get_credentials(self) -> Mapping:
        """
        Method that retrieves credentials from the store
        :return: Credentials that can be used for propagation
        """
