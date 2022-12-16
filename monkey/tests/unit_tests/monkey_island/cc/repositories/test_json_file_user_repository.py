import os
import stat

import pytest
from tests.monkey_island.utils import assert_windows_permissions

from common.utils.environment import is_windows_os
from common.utils.exceptions import (
    AlreadyRegisteredError,
    InvalidRegistrationCredentialsError,
    UnknownUserError,
)
from monkey_island.cc.models import UserCredentials
from monkey_island.cc.repositories.json_file_user_repository import (
    CREDENTIALS_FILE,
    JSONFileUserRepository,
)

USERNAME = "test"
PASSWORD_HASH = "DEADBEEF"


@pytest.fixture
def empty_datastore(tmp_path):
    return JSONFileUserRepository(tmp_path)


@pytest.fixture
def populated_datastore(data_for_tests_dir):
    return JSONFileUserRepository(data_for_tests_dir)


@pytest.fixture
def credentials_file_path(tmp_path):
    return tmp_path / CREDENTIALS_FILE


def test_has_registered_users_pre_registration(empty_datastore):
    assert not empty_datastore.has_registered_users()


def test_has_registered_users_after_registration(populated_datastore):
    assert populated_datastore.has_registered_users()


def test_add_user(empty_datastore, credentials_file_path):
    datastore = empty_datastore

    datastore.add_user(UserCredentials(USERNAME, PASSWORD_HASH))
    assert datastore.has_registered_users()
    assert credentials_file_path.exists()


@pytest.mark.skipif(is_windows_os(), reason="Tests Posix (not Windows) permissions.")
def test_add_user__term_posix(empty_datastore, credentials_file_path):
    empty_datastore.add_user(UserCredentials(USERNAME, PASSWORD_HASH))
    st = os.stat(credentials_file_path)

    expected_mode = stat.S_IRUSR | stat.S_IWUSR
    actual_mode = st.st_mode & (stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    assert expected_mode == actual_mode


@pytest.mark.skipif(not is_windows_os(), reason="Tests Windows (not Posix) permissions.")
def test_add_user__term_windows(empty_datastore, credentials_file_path):
    datastore = empty_datastore

    datastore.add_user(UserCredentials(USERNAME, PASSWORD_HASH))
    assert_windows_permissions(str(credentials_file_path))


def test_add_user__None_creds(empty_datastore):
    with pytest.raises(InvalidRegistrationCredentialsError):
        empty_datastore.add_user(None)


def test_add_user__empty_username(empty_datastore):
    with pytest.raises(InvalidRegistrationCredentialsError):
        empty_datastore.add_user(UserCredentials("", PASSWORD_HASH))


def test_add_user__empty_password_hash(empty_datastore):
    with pytest.raises(InvalidRegistrationCredentialsError):
        empty_datastore.add_user(UserCredentials(USERNAME, ""))


def test_add_user__already_registered(populated_datastore):
    with pytest.raises(AlreadyRegisteredError):
        populated_datastore.add_user(UserCredentials("new_user", "new_hash"))


def test_get_user_credentials_from_file(tmp_path):
    empty_datastore = JSONFileUserRepository(tmp_path)
    empty_datastore.add_user(UserCredentials(USERNAME, PASSWORD_HASH))

    populated_datastore = JSONFileUserRepository(tmp_path)
    stored_user = populated_datastore.get_user_credentials(USERNAME)

    assert stored_user.username == USERNAME
    assert stored_user.password_hash == PASSWORD_HASH


def test_get_unknown_user(populated_datastore):
    with pytest.raises(UnknownUserError):
        populated_datastore.get_user_credentials("unregistered_user")


def test_get_user_credentials__no_user_registered(empty_datastore):
    with pytest.raises(UnknownUserError):
        empty_datastore.get_user_credentials("unregistered_user")
