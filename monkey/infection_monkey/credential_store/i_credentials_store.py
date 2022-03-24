import abc
from typing import Mapping


class ICredentialsStore(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_credentials(self, credentials_to_add: Mapping = {}) -> None:
        """
        Method that adds credentials to the CredentialStore
        :param Credentials credentials: The credentials which will be added
        """

    @abc.abstractmethod
    def get_credentials(self) -> Mapping:
        """
        Method that gets credentials from the ControlChannel
        :return: A squence of Credentials that have been added for propagation
        :rtype: Mapping
        """
