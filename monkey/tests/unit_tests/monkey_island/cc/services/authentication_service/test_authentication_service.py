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
from monkey_island.cc.services.authentication_service.refresh_token_manager import (
    RefreshTokenManager,
)
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
def mock_repository_encryptor(autouse=True) -> ILockableEncryptor:
    return MagicMock(spec=ILockableEncryptor)


@pytest.fixture
def mock_island_event_queue(autouse=True) -> IIslandEventQueue:
    return MagicMock(spec=IIslandEventQueue)


@pytest.fixture
def mock_user_datastore(autouse=True) -> UserDatastore:
    return MagicMock(spec=UserDatastore)


@pytest.fixture
def mock_token_service(autouse=True) -> UserDatastore:
    return MagicMock(spec=RefreshTokenManager)


@pytest.fixture
def authentication_facade(
    mock_flask_app,
    mock_repository_encryptor: ILockableEncryptor,
    mock_island_event_queue: IIslandEventQueue,
    mock_user_datastore: UserDatastore,
) -> AuthenticationFacade:
    return AuthenticationFacade(
        mock_repository_encryptor, mock_island_event_queue, mock_user_datastore, mock_token_service
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
