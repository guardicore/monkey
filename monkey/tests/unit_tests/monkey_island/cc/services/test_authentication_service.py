from unittest.mock import MagicMock, call

import pytest

from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.models import IslandMode, User
from monkey_island.cc.server_utils.encryption import ILockableEncryptor
from monkey_island.cc.services import AuthenticationService

USERNAME = "user1"
PASSWORD = "test"
PASSWORD_HASH = "$2b$12$yQzymz55fRvm8rApg7erluIvIAKSFSDrNIOIrOlxC4sXsDSkeu9z2"


# Some tests have these fixtures as arguments even though `autouse=True`, because
# to access the object that a fixture returns, it needs to be specified as an argument.
# See https://stackoverflow.com/a/37046403.


@pytest.fixture
def mock_repository_encryptor(autouse=True):
    return MagicMock(spec=ILockableEncryptor)


@pytest.fixture
def mock_island_event_queue(autouse=True):
    return MagicMock(spec=IIslandEventQueue)


def test_needs_registration__true(
    mock_flask_app,
    tmp_path,
    mock_repository_encryptor,
    mock_island_event_queue,
):
    a_s = AuthenticationService(tmp_path, mock_repository_encryptor, mock_island_event_queue)

    assert a_s.needs_registration()


def test_needs_registration__false(
    monkeypatch,
    mock_flask_app,
    tmp_path,
    mock_repository_encryptor,
    mock_island_event_queue,
):
    a_s = AuthenticationService(tmp_path, mock_repository_encryptor, mock_island_event_queue)

    mock_user = MagicMock(spec=User)
    monkeypatch.setattr("monkey_island.cc.services.authentication_service.User", mock_user)
    mock_user.objects.first.return_value = User(username=USERNAME)

    assert not a_s.needs_registration()


def test_handle_successful_registration(
    mock_flask_app,
    tmp_path,
    mock_repository_encryptor,
    mock_island_event_queue,
):
    a_s = AuthenticationService(tmp_path, mock_repository_encryptor, mock_island_event_queue)

    a_s.handle_successful_registration(USERNAME, PASSWORD)

    assert mock_repository_encryptor.unlock.call_args[0][0] != USERNAME
    assert mock_repository_encryptor.unlock.call_args[0][0] != PASSWORD
    mock_repository_encryptor.reset_key.assert_called_once()
    mock_repository_encryptor.unlock.assert_called_once()

    assert mock_island_event_queue.publish.call_count == 3
    mock_island_event_queue.publish.assert_has_calls(
        [
            call(IslandEventTopic.CLEAR_SIMULATION_DATA),
            call(IslandEventTopic.RESET_AGENT_CONFIGURATION),
            call(topic=IslandEventTopic.SET_ISLAND_MODE, mode=IslandMode.UNSET),
        ]
    )


def test_handle_sucessful_logout(
    mock_flask_app,
    tmp_path,
    mock_repository_encryptor,
    mock_island_event_queue,
):
    a_s = AuthenticationService(tmp_path, mock_repository_encryptor, mock_island_event_queue)

    a_s.handle_successful_logout()

    assert mock_repository_encryptor.lock.call_count == 1
