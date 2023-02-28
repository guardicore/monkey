from pathlib import Path
from typing import Optional

from flask_security.utils import hash_password

from common.utils.exceptions import IncorrectCredentialsError, InvalidRegistrationCredentialsError
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.models import IslandMode, User
from monkey_island.cc.server_utils.encryption import ILockableEncryptor


class UserLimitError(Exception):
    """Raise when the allowed limit of users registered on the Island is being exceeded"""


class AuthenticationService:
    """
    A service for user authentication
    """

    def __init__(
        self,
        data_dir: Path,
        repository_encryptor: ILockableEncryptor,
        island_event_queue: IIslandEventQueue,
    ):
        self._data_dir = data_dir
        self._repository_encryptor = repository_encryptor
        self._island_event_queue = island_event_queue

    def needs_registration(self) -> bool:
        """
        Checks if a user is already registered on the Island

        :return: Whether registration is required on the Island
        """
        return not User.objects.first()

    def register_new_user(self, username: str, password: str):
        """
        Registers a new user on the Island, then resets the encryptor and database

        :param username: Username to register
        :param password: Password to register
        :raises InvalidRegistrationCredentialsError: If username or password is empty
        """
        if not username or not password:
            raise InvalidRegistrationCredentialsError("Username or password can not be empty.")

        if self._user_already_registered():
            raise UserLimitError(
                "A registered user already exists. To reset your credentials, follow the "
                "instructions at https://techdocs.akamai.com/infection-monkey/docs/"
                "frequently-asked-questions#reset-the-monkey-island-password."
            )

        User(username=username, password=hash_password(password)).save()

        self._island_event_queue.publish(IslandEventTopic.CLEAR_SIMULATION_DATA)
        self._island_event_queue.publish(IslandEventTopic.RESET_AGENT_CONFIGURATION)
        self._island_event_queue.publish(
            topic=IslandEventTopic.SET_ISLAND_MODE, mode=IslandMode.UNSET
        )

        self._reset_repository_encryptor(username, password)

    def _user_already_registered(self) -> Optional[User]:
        return User.objects.first()

    def authenticate(self, username: str, password: str) -> User:
        registered_user = User.objects.filter(username=username).first()

        if registered_user is None or not registered_user.verify_and_update_password(password):
            raise IncorrectCredentialsError()

        self._unlock_repository_encryptor(username, password)

        return registered_user

    def _unlock_repository_encryptor(self, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        self._repository_encryptor.unlock(secret.encode())

    def _reset_repository_encryptor(self, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        self._repository_encryptor.reset_key()
        self._repository_encryptor.unlock(secret.encode())


def _get_secret_from_credentials(username: str, password: str) -> str:
    return f"{username}:{password}"
