from unittest.mock import MagicMock, call

import pytest

from common.utils.exceptions import (
    AlreadyRegisteredError,
    IncorrectCredentialsError,
    InvalidRegistrationCredentialsError,
    UnknownUserError,
)
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.models import IslandMode, UserCredentials
from monkey_island.cc.repositories import IUserRepository
from monkey_island.cc.server_utils.encryption import ILockableEncryptor
from monkey_island.cc.services import AuthenticationService

USERNAME = "user1"
PASSWORD = "test"
PASSWORD_HASH = "$2b$12$YsGjjuJFddYJ6z5S5/nMCuKkCzKHB1AWY9SXkQ02i25d8TgdhIRS2"


class MockUserDatastore(IUserRepository):
    def __init__(self, has_registered_users, add_user, get_user_credentials):
        self._has_registered_users = has_registered_users
        self._add_user = add_user
        self._get_user_credentials = get_user_credentials

    def has_registered_users(self):
        return self._has_registered_users()

    def add_user(self, credentials: UserCredentials):
        return self._add_user(credentials)

    def get_user_credentials(self, username: str) -> UserCredentials:
        return self._get_user_credentials(username)


# Some tests have these fixtures as arguments even though `autouse=True`, because
# to access the object that a fixture returns, it needs to be specified as an argument.
# See https://stackoverflow.com/a/37046403.


@pytest.fixture
def mock_repository_encryptor(autouse=True):
    return MagicMock(spec=ILockableEncryptor)


@pytest.fixture
def mock_island_event_queue(autouse=True):
    return MagicMock(spec=IIslandEventQueue)


def test_needs_registration__true(tmp_path):
    has_registered_users = False
    mock_user_datastore = MockUserDatastore(lambda: has_registered_users, None, None)

    a_s = AuthenticationService(
        tmp_path, mock_user_datastore, mock_repository_encryptor, mock_island_event_queue
    )

    assert a_s.needs_registration()


def test_needs_registration__false(tmp_path):
    has_registered_users = True
    mock_user_datastore = MockUserDatastore(lambda: has_registered_users, None, None)

    a_s = AuthenticationService(
        tmp_path, mock_user_datastore, mock_repository_encryptor, mock_island_event_queue
    )

    assert not a_s.needs_registration()


@pytest.mark.slow
@pytest.mark.parametrize("error", [InvalidRegistrationCredentialsError, AlreadyRegisteredError])
def test_register_new_user__fails(tmp_path, mock_repository_encryptor, error):
    mock_user_datastore = MockUserDatastore(lambda: True, MagicMock(side_effect=error), None)

    a_s = AuthenticationService(
        tmp_path, mock_user_datastore, mock_repository_encryptor, mock_island_event_queue
    )

    with pytest.raises(error):
        a_s.register_new_user(USERNAME, PASSWORD)

    mock_repository_encryptor.reset_key().assert_not_called()
    mock_repository_encryptor.unlock.assert_not_called()


@pytest.mark.slow
@pytest.mark.parametrize("error", [InvalidRegistrationCredentialsError, AlreadyRegisteredError])
def test_register_new_user_fails__publish_to_event_topic(tmp_path, error, mock_island_event_queue):
    mock_user_datastore = MockUserDatastore(lambda: True, MagicMock(side_effect=error), None)

    a_s = AuthenticationService(
        tmp_path, mock_user_datastore, mock_repository_encryptor, mock_island_event_queue
    )

    with pytest.raises(error):
        a_s.register_new_user(USERNAME, PASSWORD)

    mock_island_event_queue.publish.assert_not_called()


def test_register_new_user__empty_password_fails(
    tmp_path, mock_repository_encryptor, mock_island_event_queue
):
    mock_user_datastore = MockUserDatastore(lambda: False, None, None)

    a_s = AuthenticationService(
        tmp_path, mock_user_datastore, mock_repository_encryptor, mock_island_event_queue
    )

    with pytest.raises(InvalidRegistrationCredentialsError):
        a_s.register_new_user(USERNAME, "")

    mock_repository_encryptor.reset_key().assert_not_called()
    mock_repository_encryptor.unlock.assert_not_called()
    mock_island_event_queue.publish.assert_not_called()


@pytest.mark.slow
def test_register_new_user(tmp_path, mock_repository_encryptor, mock_island_event_queue):
    mock_add_user = MagicMock()
    mock_user_datastore = MockUserDatastore(lambda: False, mock_add_user, None)

    a_s = AuthenticationService(
        tmp_path, mock_user_datastore, mock_repository_encryptor, mock_island_event_queue
    )

    a_s.register_new_user(USERNAME, PASSWORD)

    assert mock_add_user.call_args[0][0].username == USERNAME
    assert mock_add_user.call_args[0][0].password_hash != PASSWORD

    mock_repository_encryptor.reset_key.assert_called_once()
    mock_repository_encryptor.unlock.assert_called_once()
    assert mock_repository_encryptor.unlock.call_args[0][0] != USERNAME


@pytest.mark.slow
def test_register_new_user__publish_to_event_topics(
    tmp_path, mock_repository_encryptor, mock_island_event_queue
):
    mock_add_user = MagicMock()
    mock_user_datastore = MockUserDatastore(lambda: False, mock_add_user, None)

    a_s = AuthenticationService(
        tmp_path, mock_user_datastore, mock_repository_encryptor, mock_island_event_queue
    )

    a_s.register_new_user(USERNAME, PASSWORD)

    assert mock_island_event_queue.publish.call_count == 3
    mock_island_event_queue.publish.assert_has_calls(
        [
            call(IslandEventTopic.CLEAR_SIMULATION_DATA),
            call(IslandEventTopic.RESET_AGENT_CONFIGURATION),
            call(topic=IslandEventTopic.SET_ISLAND_MODE, mode=IslandMode.UNSET),
        ]
    )


@pytest.mark.slow
def test_authenticate__success(tmp_path, mock_repository_encryptor):
    mock_user_datastore = MockUserDatastore(
        lambda: True,
        None,
        lambda _: UserCredentials(USERNAME, PASSWORD_HASH),
    )

    a_s = AuthenticationService(
        tmp_path, mock_user_datastore, mock_repository_encryptor, mock_island_event_queue
    )

    # If authentication fails, this function will raise an exception and the test will fail.
    a_s.authenticate(USERNAME, PASSWORD)
    mock_repository_encryptor.unlock.assert_called_once()


@pytest.mark.slow
@pytest.mark.parametrize(
    ("username", "password"), [("wrong_username", PASSWORD), (USERNAME, "wrong_password")]
)
def test_authenticate__failed_wrong_credentials(
    tmp_path, username, password, mock_repository_encryptor
):
    mock_user_datastore = MockUserDatastore(
        lambda: True,
        None,
        lambda _: UserCredentials(USERNAME, PASSWORD_HASH),
    )

    a_s = AuthenticationService(
        tmp_path, mock_user_datastore, mock_repository_encryptor, mock_island_event_queue
    )

    with pytest.raises(IncorrectCredentialsError):
        a_s.authenticate(username, password)

    mock_repository_encryptor.unlock.assert_not_called()


def test_authenticate__failed_no_registered_user(tmp_path, mock_repository_encryptor):
    mock_user_datastore = MockUserDatastore(
        lambda: True, None, MagicMock(side_effect=UnknownUserError)
    )

    a_s = AuthenticationService(
        tmp_path, mock_user_datastore, mock_repository_encryptor, mock_island_event_queue
    )

    with pytest.raises(IncorrectCredentialsError):
        a_s.authenticate(USERNAME, PASSWORD)

    mock_repository_encryptor.unlock.assert_not_called()
