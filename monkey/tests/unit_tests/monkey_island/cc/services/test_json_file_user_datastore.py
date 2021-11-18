import pytest

from common.utils.exceptions import (
    AlreadyRegisteredError,
    InvalidRegistrationCredentialsError,
    UnknownUserError,
)
from monkey_island.cc.environment.user_creds import UserCreds
from monkey_island.cc.services.authentication.json_file_user_datastore import (
    CREDENTIALS_FILE,
    JsonFileUserDatastore,
)

USERNAME = "test"
PASSWORD_HASH = "DEADBEEF"


@pytest.fixture
def empty_datastore(tmp_path):
    return JsonFileUserDatastore(tmp_path)


@pytest.fixture
def populated_datastore(data_for_tests_dir):
    return JsonFileUserDatastore(data_for_tests_dir)


def test_has_registered_users_pre_registration(empty_datastore):
    assert not empty_datastore.has_registered_users()


def test_has_registered_users_after_registration(populated_datastore):
    assert populated_datastore.has_registered_users()


def test_add_user(empty_datastore, tmp_path):
    datastore = empty_datastore

    datastore.add_user(UserCreds(USERNAME, PASSWORD_HASH))
    assert datastore.has_registered_users()
    assert (tmp_path / CREDENTIALS_FILE).exists()


def test_add_user__None_creds(empty_datastore):
    with pytest.raises(InvalidRegistrationCredentialsError):
        empty_datastore.add_user(None)


def test_add_user__empty_username(empty_datastore):
    with pytest.raises(InvalidRegistrationCredentialsError):
        empty_datastore.add_user(UserCreds("", PASSWORD_HASH))


def test_add_user__empty_password_hash(empty_datastore):
    with pytest.raises(InvalidRegistrationCredentialsError):
        empty_datastore.add_user(UserCreds(USERNAME, ""))


def test_add_user__already_registered(populated_datastore):
    with pytest.raises(AlreadyRegisteredError):
        populated_datastore.add_user(UserCreds("new_user", "new_hash"))


def test_get_user_credentials_from_file(tmp_path):
    empty_datastore = JsonFileUserDatastore(tmp_path)
    empty_datastore.add_user(UserCreds(USERNAME, PASSWORD_HASH))

    populated_datastore = JsonFileUserDatastore(tmp_path)
    stored_user = populated_datastore.get_user_credentials(USERNAME)

    assert stored_user.username == USERNAME
    assert stored_user.password_hash == PASSWORD_HASH


def test_get_unknown_user(populated_datastore):
    with pytest.raises(UnknownUserError):
        populated_datastore.get_user_credentials("unregistered_user")
