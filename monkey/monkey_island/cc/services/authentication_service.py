from pathlib import Path

import bcrypt

from common.utils.exceptions import (
    IncorrectCredentialsError,
    InvalidRegistrationCredentialsError,
    UnknownUserError,
)
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.models import IslandMode, UserCredentials
from monkey_island.cc.repositories import IUserRepository
from monkey_island.cc.server_utils.encryption import ILockableEncryptor


class AuthenticationService:
    """
    A service for user authentication
    """

    def __init__(
        self,
        data_dir: Path,
        user_repository: IUserRepository,
        repository_encryptor: ILockableEncryptor,
        island_event_queue: IIslandEventQueue,
    ):
        self._data_dir = data_dir
        self._user_repository = user_repository
        self._repository_encryptor = repository_encryptor
        self._island_event_queue = island_event_queue

    def needs_registration(self) -> bool:
        """
        Checks if a user is already registered on the Island

        :return: Whether registration is required on the Island
        """
        return not self._user_repository.has_registered_users()

    def register_new_user(self, username: str, password: str):
        """
        Registers a new user on the Island, then resets the encryptor and database

        :param username: Username to register
        :param password: Password to register
        :raises InvalidRegistrationCredentialsError: If username or password is empty
        """
        if not username or not password:
            raise InvalidRegistrationCredentialsError("Username or password can not be empty.")

        credentials = UserCredentials(username, _hash_password(password))
        self._user_repository.add_user(credentials)

        self._island_event_queue.publish(IslandEventTopic.CLEAR_SIMULATION_DATA)
        self._island_event_queue.publish(IslandEventTopic.RESET_AGENT_CONFIGURATION)
        self._island_event_queue.publish(
            topic=IslandEventTopic.SET_ISLAND_MODE, mode=IslandMode.UNSET
        )

        self._reset_repository_encryptor(username, password)

    def authenticate(self, username: str, password: str):
        try:
            registered_user = self._user_repository.get_user_credentials(username)
        except UnknownUserError:
            raise IncorrectCredentialsError()

        if not _credentials_match_registered_user(username, password, registered_user):
            raise IncorrectCredentialsError()

        self._unlock_repository_encryptor(username, password)

    def _unlock_repository_encryptor(self, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        self._repository_encryptor.unlock(secret.encode())

    def _reset_repository_encryptor(self, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        self._repository_encryptor.reset_key()
        self._repository_encryptor.unlock(secret.encode())


def _hash_password(plaintext_password: str) -> str:
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(plaintext_password.encode("utf-8"), salt)

    return password_hash.decode()


def _credentials_match_registered_user(
    username: str, password: str, registered_user: UserCredentials
) -> bool:
    return (registered_user.username == username) and _password_matches_hash(
        password, registered_user.password_hash
    )


def _password_matches_hash(plaintext_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plaintext_password.encode("utf-8"), password_hash.encode("utf-8"))


def _get_secret_from_credentials(username: str, password: str) -> str:
    return f"{username}:{password}"
