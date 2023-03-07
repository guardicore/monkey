from pathlib import Path
from typing import Dict

from flask_security import UserDatastore

from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.models import IslandMode, User
from monkey_island.cc.server_utils.encryption import ILockableEncryptor


class AuthenticationService:
    """
    A service for user authentication
    """

    def __init__(
        self,
        data_dir: Path,
        repository_encryptor: ILockableEncryptor,
        island_event_queue: IIslandEventQueue,
        user_datastore: UserDatastore,
    ):
        self._data_dir = data_dir
        self._repository_encryptor = repository_encryptor
        self._island_event_queue = island_event_queue
        self._user_datastore = user_datastore

    def needs_registration(self) -> bool:
        """
        Checks if a user is already registered on the Island

        :return: Whether registration is required on the Island
        """
        return not User.objects.first()

    def apply_role_to_user(self, username: str, role_fields: Dict[str, str]):
        user = self._user_datastore.find_user(username=username)
        role = self._user_datastore.find_or_create_role(**role_fields)

        self._user_datastore.add_role_to_user(user=user, role=role)

    def reset_island_data(self):
        """
        Resets the island
        """
        self._island_event_queue.publish(IslandEventTopic.CLEAR_SIMULATION_DATA)
        self._island_event_queue.publish(IslandEventTopic.RESET_AGENT_CONFIGURATION)
        self._island_event_queue.publish(
            topic=IslandEventTopic.SET_ISLAND_MODE, mode=IslandMode.UNSET
        )

    def reset_repository_encryptor(self, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        self._repository_encryptor.reset_key()
        self._repository_encryptor.unlock(secret.encode())

    def unlock_repository_encryptor(self, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        self._repository_encryptor.unlock(secret.encode())

    def lock_repository_encryptor(self):
        self._repository_encryptor.lock()


def _get_secret_from_credentials(username: str, password: str) -> str:
    return f"{username}:{password}"
