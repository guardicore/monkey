from unittest.mock import MagicMock

import pytest

from common.utils.exceptions import (
    AlreadyRegisteredError,
    IncorrectCredentialsError,
    InvalidRegistrationCredentialsError,
    UnknownUserError,
)
from monkey_island.cc.services import AuthenticationService
from monkey_island.cc.services.authentication import authentication_service
from monkey_island.cc.services.authentication.i_user_datastore import IUserDatastore
from monkey_island.cc.services.authentication.user_creds import UserCreds

USERNAME = "user1"
PASSWORD = "test"
PASSWORD_HASH = "$2b$12$YsGjjuJFddYJ6z5S5/nMCuKkCzKHB1AWY9SXkQ02i25d8TgdhIRS2"


class MockUserDatastore(IUserDatastore):
    def __init__(self, has_registered_users, add_user, get_user_credentials):
        self._has_registered_users = has_registered_users
        self._add_user = add_user
        self._get_user_credentials = get_user_credentials

    def has_registered_users(self):
        return self._has_registered_users()

    def add_user(self, credentials: UserCreds):
        return self._add_user(credentials)

    def get_user_credentials(self, username: str) -> UserCreds:
        return self._get_user_credentials(username)


@pytest.fixture
def mock_reset_datastore_encryptor():
    return MagicMock()


@pytest.fixture
def mock_reset_database():
    return MagicMock()


@pytest.fixture
def mock_unlock_datastore_encryptor():
    return MagicMock()


@pytest.fixture(autouse=True)
def patch_datastore_utils(
    monkeypatch,
    mock_reset_datastore_encryptor,
    mock_reset_database,
    mock_unlock_datastore_encryptor,
):
    monkeypatch.setattr(
        authentication_service, "reset_datastore_encryptor", mock_reset_datastore_encryptor
    )
    monkeypatch.setattr(authentication_service, "reset_database", mock_reset_database)
    monkeypatch.setattr(
        authentication_service, "unlock_datastore_encryptor", mock_unlock_datastore_encryptor
    )


def test_needs_registration__true(tmp_path):
    has_registered_users = False
    mock_user_datastore = MockUserDatastore(lambda: has_registered_users, None, None)

    a_s = AuthenticationService()
    a_s.initialize(tmp_path, mock_user_datastore)

    assert a_s.needs_registration()


def test_needs_registration__false(tmp_path):
    has_registered_users = True
    mock_user_datastore = MockUserDatastore(lambda: has_registered_users, None, None)

    a_s = AuthenticationService()
    a_s.initialize(tmp_path, mock_user_datastore)

    assert not a_s.needs_registration()


@pytest.mark.slow
@pytest.mark.parametrize("error", [InvalidRegistrationCredentialsError, AlreadyRegisteredError])
def test_register_new_user__fails(
    tmp_path, mock_reset_datastore_encryptor, mock_reset_database, error
):
    mock_user_datastore = MockUserDatastore(lambda: True, MagicMock(side_effect=error), None)

    a_s = AuthenticationService()
    a_s.initialize(tmp_path, mock_user_datastore)

    with pytest.raises(error):
        a_s.register_new_user(USERNAME, PASSWORD)

    mock_reset_datastore_encryptor.assert_not_called()
    mock_reset_database.assert_not_called()


def test_register_new_user__empty_password_fails(
    tmp_path, mock_reset_datastore_encryptor, mock_reset_database
):
    mock_user_datastore = MockUserDatastore(lambda: False, None, None)

    a_s = AuthenticationService()
    a_s.initialize(tmp_path, mock_user_datastore)

    with pytest.raises(InvalidRegistrationCredentialsError):
        a_s.register_new_user(USERNAME, "")

    mock_reset_datastore_encryptor.assert_not_called()
    mock_reset_database.assert_not_called()


@pytest.mark.slow
def test_register_new_user(tmp_path, mock_reset_datastore_encryptor, mock_reset_database):
    mock_add_user = MagicMock()
    mock_user_datastore = MockUserDatastore(lambda: False, mock_add_user, None)

    a_s = AuthenticationService()
    a_s.initialize(tmp_path, mock_user_datastore)

    a_s.register_new_user(USERNAME, PASSWORD)

    assert mock_add_user.call_args[0][0].username == USERNAME
    assert mock_add_user.call_args[0][0].password_hash != PASSWORD

    mock_reset_datastore_encryptor.assert_called_once()
    assert mock_reset_datastore_encryptor.call_args[0][1] != USERNAME

    mock_reset_database.assert_called_once()


@pytest.mark.slow
def test_authenticate__success(tmp_path, mock_unlock_datastore_encryptor):
    mock_user_datastore = MockUserDatastore(
        lambda: True,
        None,
        lambda _: UserCreds(USERNAME, PASSWORD_HASH),
    )

    a_s = AuthenticationService()
    a_s.initialize(tmp_path, mock_user_datastore)

    # If authentication fails, this function will raise an exception and the test will fail.
    a_s.authenticate(USERNAME, PASSWORD)
    mock_unlock_datastore_encryptor.assert_called_once()


@pytest.mark.slow
@pytest.mark.parametrize(
    ("username", "password"), [("wrong_username", PASSWORD), (USERNAME, "wrong_password")]
)
def test_authenticate__failed_wrong_credentials(
    tmp_path, mock_unlock_datastore_encryptor, username, password
):
    mock_user_datastore = MockUserDatastore(
        lambda: True,
        None,
        lambda _: UserCreds(USERNAME, PASSWORD_HASH),
    )

    a_s = AuthenticationService()
    a_s.initialize(tmp_path, mock_user_datastore)

    with pytest.raises(IncorrectCredentialsError):
        a_s.authenticate(username, password)

    mock_unlock_datastore_encryptor.assert_not_called()


def test_authenticate__failed_no_registered_user(tmp_path, mock_unlock_datastore_encryptor):
    mock_user_datastore = MockUserDatastore(
        lambda: True, None, MagicMock(side_effect=UnknownUserError)
    )

    a_s = AuthenticationService()
    a_s.initialize(tmp_path, mock_user_datastore)

    with pytest.raises(IncorrectCredentialsError):
        a_s.authenticate(USERNAME, PASSWORD)

    mock_unlock_datastore_encryptor.assert_not_called()
