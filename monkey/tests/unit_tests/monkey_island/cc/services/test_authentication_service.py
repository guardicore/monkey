from unittest.mock import MagicMock

import pytest

from common.utils.exceptions import (
    AlreadyRegisteredError,
    IncorrectCredentialsError,
    InvalidRegistrationCredentialsError,
    UnknownUserError,
)
from monkey_island.cc.models import UserCredentials
from monkey_island.cc.repository import IUserRepository
from monkey_island.cc.server_utils.encryption import ILockableEncryptor
from monkey_island.cc.services import AuthenticationService, authentication_service

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


@pytest.fixture
def mock_reset_datastore_encryptor():
    return MagicMock()


@pytest.fixture
def mock_unlock_datastore_encryptor():
    return MagicMock()


@pytest.fixture
def mock_repository_encryptor():
    return MagicMock(spec=ILockableEncryptor)


@pytest.fixture(autouse=True)
def patch_datastore_utils(
    monkeypatch,
    mock_reset_datastore_encryptor,
    mock_unlock_datastore_encryptor,
):
    monkeypatch.setattr(
        authentication_service, "reset_datastore_encryptor", mock_reset_datastore_encryptor
    )
    monkeypatch.setattr(
        authentication_service, "unlock_datastore_encryptor", mock_unlock_datastore_encryptor
    )


def test_needs_registration__true(tmp_path, mock_repository_encryptor):
    has_registered_users = False
    mock_user_datastore = MockUserDatastore(lambda: has_registered_users, None, None)

    a_s = AuthenticationService(tmp_path, mock_user_datastore, mock_repository_encryptor)

    assert a_s.needs_registration()


def test_needs_registration__false(tmp_path, mock_repository_encryptor):
    has_registered_users = True
    mock_user_datastore = MockUserDatastore(lambda: has_registered_users, None, None)

    a_s = AuthenticationService(tmp_path, mock_user_datastore, mock_repository_encryptor)

    assert not a_s.needs_registration()


@pytest.mark.slow
@pytest.mark.parametrize("error", [InvalidRegistrationCredentialsError, AlreadyRegisteredError])
def test_register_new_user__fails(
    tmp_path, mock_reset_datastore_encryptor, mock_repository_encryptor, error
):
    mock_user_datastore = MockUserDatastore(lambda: True, MagicMock(side_effect=error), None)

    a_s = AuthenticationService(tmp_path, mock_user_datastore, mock_repository_encryptor)

    with pytest.raises(error):
        a_s.register_new_user(USERNAME, PASSWORD)

    mock_reset_datastore_encryptor.assert_not_called()
    mock_repository_encryptor.reset_key().assert_not_called()
    mock_repository_encryptor.unlock.assert_not_called()


def test_register_new_user__empty_password_fails(
    tmp_path, mock_reset_datastore_encryptor, mock_repository_encryptor
):
    mock_user_datastore = MockUserDatastore(lambda: False, None, None)

    a_s = AuthenticationService(tmp_path, mock_user_datastore, mock_repository_encryptor)

    with pytest.raises(InvalidRegistrationCredentialsError):
        a_s.register_new_user(USERNAME, "")

    mock_reset_datastore_encryptor.assert_not_called()
    mock_repository_encryptor.reset_key().assert_not_called()
    mock_repository_encryptor.unlock.assert_not_called()


@pytest.mark.slow
def test_register_new_user(tmp_path, mock_reset_datastore_encryptor, mock_repository_encryptor):
    mock_add_user = MagicMock()
    mock_user_datastore = MockUserDatastore(lambda: False, mock_add_user, None)

    a_s = AuthenticationService(tmp_path, mock_user_datastore, mock_repository_encryptor)

    a_s.register_new_user(USERNAME, PASSWORD)

    assert mock_add_user.call_args[0][0].username == USERNAME
    assert mock_add_user.call_args[0][0].password_hash != PASSWORD

    mock_reset_datastore_encryptor.assert_called_once()
    assert mock_reset_datastore_encryptor.call_args[0][1] != USERNAME

    mock_repository_encryptor.reset_key.assert_called_once()
    mock_repository_encryptor.unlock.assert_called_once()
    assert mock_repository_encryptor.unlock.call_args[0][0] != USERNAME


@pytest.mark.slow
def test_authenticate__success(
    tmp_path, mock_unlock_datastore_encryptor, mock_repository_encryptor
):
    mock_user_datastore = MockUserDatastore(
        lambda: True,
        None,
        lambda _: UserCredentials(USERNAME, PASSWORD_HASH),
    )

    a_s = AuthenticationService(tmp_path, mock_user_datastore, mock_repository_encryptor)

    # If authentication fails, this function will raise an exception and the test will fail.
    a_s.authenticate(USERNAME, PASSWORD)
    mock_unlock_datastore_encryptor.assert_called_once()
    mock_repository_encryptor.unlock.assert_called_once()


@pytest.mark.slow
@pytest.mark.parametrize(
    ("username", "password"), [("wrong_username", PASSWORD), (USERNAME, "wrong_password")]
)
def test_authenticate__failed_wrong_credentials(
    tmp_path, mock_unlock_datastore_encryptor, username, password, mock_repository_encryptor
):
    mock_user_datastore = MockUserDatastore(
        lambda: True,
        None,
        lambda _: UserCredentials(USERNAME, PASSWORD_HASH),
    )

    a_s = AuthenticationService(tmp_path, mock_user_datastore, mock_repository_encryptor)

    with pytest.raises(IncorrectCredentialsError):
        a_s.authenticate(username, password)

    mock_unlock_datastore_encryptor.assert_not_called()
    mock_repository_encryptor.unlock.assert_not_called()


def test_authenticate__failed_no_registered_user(
    tmp_path, mock_unlock_datastore_encryptor, mock_repository_encryptor
):
    mock_user_datastore = MockUserDatastore(
        lambda: True, None, MagicMock(side_effect=UnknownUserError)
    )

    a_s = AuthenticationService(tmp_path, mock_user_datastore, mock_repository_encryptor)

    with pytest.raises(IncorrectCredentialsError):
        a_s.authenticate(USERNAME, PASSWORD)

    mock_unlock_datastore_encryptor.assert_not_called()
    mock_repository_encryptor.unlock.assert_not_called()
