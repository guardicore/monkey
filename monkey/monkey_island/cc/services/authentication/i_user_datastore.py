import abc

from .user_creds import UserCreds


class IUserDatastore(metaclass=abc.ABCMeta):
    """
    Allows user credentials to be stored and retrieved.
    """

    @abc.abstractmethod
    def has_registered_users(self) -> bool:
        """
        Checks if there are any registered user.
        :return: True if any users have been registered, False otherwise
        :rtype: bool
        """

    @abc.abstractmethod
    def add_user(self, credentials: UserCreds):
        """
        Adds a new user to the datastore.
        :param UserCreds credentials: New user credentials to persistant storage.
        :raises InvalidRegistrationCredentialsError: if the credentials are malformed
        :raises AlreadyRegisteredError: if the user has already been registered
        """

    @abc.abstractmethod
    def get_user_credentials(self, username: str) -> UserCreds:
        """
        Gets the user matching `username` from storage.
        :param str username: The username for which credentials will be retrieved
        :return: User credentials for username
        :rtype: UserCreds
        :raises UnknownUserError: if the username does not exist
        """
