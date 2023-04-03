from typing import Tuple

from flask_security import UserDatastore

from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.models import IslandMode
from monkey_island.cc.server_utils.encryption import ILockableEncryptor
from monkey_island.cc.services.authentication_service.token.token_generator import TokenGenerator

from . import AccountRole
from .token import ParsedToken, Token, TokenParser
from .user import User


class AuthenticationFacade:
    """
    A service for user authentication
    """

    def __init__(
        self,
        repository_encryptor: ILockableEncryptor,
        island_event_queue: IIslandEventQueue,
        user_datastore: UserDatastore,
        token_generator: TokenGenerator,
        token_parser: TokenParser,
    ):
        self._repository_encryptor = repository_encryptor
        self._island_event_queue = island_event_queue
        self._datastore = user_datastore
        self._token_generator = token_generator
        self._token_parser = token_parser

    def needs_registration(self) -> bool:
        """
        Checks if a user is already registered on the Island

        :return: Whether registration is required on the Island
        """
        island_api_user_role = self._datastore.find_or_create_role(
            name=AccountRole.ISLAND_INTERFACE.name
        )
        return not self._datastore.find_user(roles=[island_api_user_role])

    def revoke_all_tokens_for_user(self, user: User):
        """
        Revokes all tokens for a specific user
        """
        self._datastore.set_uniquifier(user)

    def generate_new_token_pair(self, refresh_token: Token) -> Tuple[Token, Token]:
        """
        Generates a new access token and refresh, given a valid refresh token

        :param refresh_token: Refresh token
        :raise TokenValidationError: If the refresh token is invalid or expired
        :return: Tuple of the new access token and refresh token
        """
        parsed_refresh_token = self._token_parser.parse(refresh_token)
        user = self._get_refresh_token_owner(parsed_refresh_token)

        new_access_token = user.get_auth_token()
        new_refresh_token = self._token_generator.generate_token(user.fs_uniquifier)

        return new_access_token, new_refresh_token

    def _get_refresh_token_owner(self, refresh_token: ParsedToken) -> User:
        user = self._datastore.find_user(fs_uniquifier=refresh_token.user_uniquifier)
        if not user:
            raise Exception("Invalid refresh token")
        return user

    def generate_refresh_token(self, user: User) -> Token:
        """
        Generates a refresh token for a specific user
        """
        return self._token_generator.generate_token(user.fs_uniquifier)

    def revoke_all_tokens_for_all_users(self):
        """
        Revokes all tokens for all users
        """
        for user in User.objects:
            self.revoke_all_tokens_for_user(user)

    def handle_successful_registration(self, username: str, password: str):
        self._reset_island_data()
        self._reset_repository_encryptor(username, password)

    def _reset_island_data(self):
        """
        Resets the island
        """
        self._island_event_queue.publish(IslandEventTopic.CLEAR_SIMULATION_DATA)
        self._island_event_queue.publish(IslandEventTopic.RESET_AGENT_CONFIGURATION)
        self._island_event_queue.publish(
            topic=IslandEventTopic.SET_ISLAND_MODE, mode=IslandMode.UNSET
        )

    def _reset_repository_encryptor(self, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        self._repository_encryptor.reset_key()
        self._repository_encryptor.unlock(secret.encode())

    def handle_successful_login(self, username: str, password: str):
        self._unlock_repository_encryptor(username, password)

    def _unlock_repository_encryptor(self, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        self._repository_encryptor.unlock(secret.encode())


def _get_secret_from_credentials(username: str, password: str) -> str:
    return f"{username}:{password}"
