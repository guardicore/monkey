from unittest.mock import MagicMock, call

import pytest
from flask_security import UserDatastore
from tests.common import StubDIContainer

from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.models import IslandMode
from monkey_island.cc.server_utils.encryption import ILockableEncryptor
from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)
from monkey_island.cc.services.authentication_service.setup import setup_authentication
from monkey_island.cc.services.authentication_service.token import TokenGenerator, TokenValidator
from monkey_island.cc.services.authentication_service.user import User

USERNAME = "user1"
PASSWORD = "test"
PASSWORD_HASH = "$2b$12$yQzymz55fRvm8rApg7erluIvIAKSFSDrNIOIrOlxC4sXsDSkeu9z2"
USERS = [
    User(username="user1", password="test1", fs_uniquifier="a"),
    User(username="user2", password="test2", fs_uniquifier="b"),
    User(username="user3", password="test3", fs_uniquifier="c"),
]


# Some tests have these fixtures as arguments even though `autouse=True`, because
# to access the object that a fixture returns, it needs to be specified as an argument.
# See https://stackoverflow.com/a/37046403.


@pytest.fixture
def mock_repository_encryptor() -> ILockableEncryptor:
    return MagicMock(spec=ILockableEncryptor)


@pytest.fixture
def mock_island_event_queue() -> IIslandEventQueue:
    return MagicMock(spec=IIslandEventQueue)


@pytest.fixture
def mock_user_datastore() -> UserDatastore:
    return MagicMock(spec=UserDatastore)


@pytest.fixture
def mock_token_generator() -> UserDatastore:
    return MagicMock(spec=TokenGenerator)


@pytest.fixture
def mock_token_validator() -> UserDatastore:
    return MagicMock(spec=TokenValidator)


@pytest.fixture
def authentication_facade(
    mock_flask_app,
    mock_repository_encryptor: ILockableEncryptor,
    mock_island_event_queue: IIslandEventQueue,
    mock_user_datastore: UserDatastore,
    mock_token_generator: TokenGenerator,
    mock_token_validator: TokenValidator,
) -> AuthenticationFacade:
    return AuthenticationFacade(
        mock_repository_encryptor,
        mock_island_event_queue,
        mock_user_datastore,
        mock_token_generator,
        mock_token_validator,
    )


def test_needs_registration__true(authentication_facade: AuthenticationFacade):
    assert authentication_facade.needs_registration()


def test_needs_registration__false(
    monkeypatch,
    authentication_facade: AuthenticationFacade,
):
    User(username=USERNAME, password=PASSWORD).save()
    assert not authentication_facade.needs_registration()


def test_handle_successful_registration(
    mock_repository_encryptor: ILockableEncryptor,
    mock_island_event_queue: IIslandEventQueue,
    authentication_facade: AuthenticationFacade,
):
    authentication_facade.handle_successful_registration(USERNAME, PASSWORD)

    assert mock_repository_encryptor.unlock.call_args[0][0] != USERNAME
    assert mock_repository_encryptor.unlock.call_args[0][0] != PASSWORD
    assert mock_island_event_queue.publish.call_count == 3
    mock_repository_encryptor.reset_key.assert_called_once()
    mock_repository_encryptor.unlock.assert_called_once()
    mock_island_event_queue.publish.assert_has_calls(
        [
            call(IslandEventTopic.CLEAR_SIMULATION_DATA),
            call(IslandEventTopic.RESET_AGENT_CONFIGURATION),
            call(topic=IslandEventTopic.SET_ISLAND_MODE, mode=IslandMode.UNSET),
        ]
    )


def test_handle_sucessful_login(
    mock_repository_encryptor: ILockableEncryptor,
    authentication_facade: AuthenticationFacade,
):
    authentication_facade.handle_successful_login(USERNAME, PASSWORD)

    mock_repository_encryptor.unlock.assert_called_once()
    assert mock_repository_encryptor.unlock.call_args[0][0] != USERNAME
    assert mock_repository_encryptor.unlock.call_args[0][0] != PASSWORD


def test_generate_new_token_pair__generates_tokens(
    mock_token_generator: TokenGenerator,
    mock_token_validator: TokenValidator,
    authentication_facade: AuthenticationFacade,
):
    refresh_token = "original_token"
    user = User(username=USERNAME, password=PASSWORD, fs_uniquifier="a")
    user.save()
    mock_token_generator.generate_token.return_value = "new_token"
    mock_token_validator.get_token_payload.return_value = "a"
    access_token, new_refresh_token = authentication_facade.generate_new_token_pair(refresh_token)

    assert new_refresh_token != refresh_token
    assert access_token != refresh_token
    assert access_token != new_refresh_token


def test_generate_new_token_pair__fails_if_user_does_not_exist(
    authentication_facade: AuthenticationFacade,
):
    user = User(username=USERNAME, password=PASSWORD, fs_uniquifier="a")
    refresh_token = authentication_facade.generate_refresh_token(user)

    with pytest.raises(Exception):
        authentication_facade.generate_new_token_pair(refresh_token)


def test_generate_new_token_pair__fails_if_refresh_token_expired(
    mock_token_validator: TokenValidator,
    authentication_facade: AuthenticationFacade,
):
    user = User(username=USERNAME, password=PASSWORD, fs_uniquifier="a")
    user.save()
    refresh_token = authentication_facade.generate_refresh_token(user)
    mock_token_validator.get_token_payload.side_effect = Exception()

    with pytest.raises(Exception):
        authentication_facade.generate_new_token_pair(refresh_token)


def test_revoke_all_tokens_for_all_users(
    mock_user_datastore: UserDatastore,
    authentication_facade: AuthenticationFacade,
):
    [user.save() for user in USERS]
    authentication_facade.revoke_all_tokens_for_all_users()

    assert mock_user_datastore.set_uniquifier.call_count == len(USERS)
    [mock_user_datastore.set_uniquifier.assert_any_call(user) for user in USERS]


def test_setup_authentication__revokes_tokens(
    mock_island_event_queue: IIslandEventQueue,
    mock_repository_encryptor: ILockableEncryptor,
    mock_authentication_facade: AuthenticationFacade,
):
    container = StubDIContainer()
    container.register_instance(ILockableEncryptor, mock_repository_encryptor)
    container.register_instance(IIslandEventQueue, mock_island_event_queue)
    setup_authentication(MagicMock(), mock_authentication_facade)

    assert mock_authentication_facade.revoke_all_tokens_for_all_users.called
