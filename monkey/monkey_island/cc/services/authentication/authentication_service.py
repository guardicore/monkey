from pathlib import Path

import bcrypt

from common.utils.exceptions import (
    IncorrectCredentialsError,
    InvalidRegistrationCredentialsError,
    UnknownUserError,
)
from monkey_island.cc.server_utils.encryption import (
    reset_datastore_encryptor,
    unlock_datastore_encryptor,
)
from monkey_island.cc.setup.mongo.database_initializer import reset_database

from .i_user_datastore import IUserDatastore
from .user_creds import UserCreds


class AuthenticationService:
    def __init__(self, data_dir: Path, user_datastore: IUserDatastore):
        self._data_dir = data_dir
        self._user_datastore = user_datastore

    def needs_registration(self) -> bool:
        return not self._user_datastore.has_registered_users()

    def register_new_user(self, username: str, password: str):
        if not username or not password:
            raise InvalidRegistrationCredentialsError("Username or password can not be empty.")

        credentials = UserCreds(username, _hash_password(password))
        self._user_datastore.add_user(credentials)
        self._reset_datastore_encryptor(username, password)
        reset_database()

    def authenticate(self, username: str, password: str):
        try:
            registered_user = self._user_datastore.get_user_credentials(username)
        except UnknownUserError:
            raise IncorrectCredentialsError()

        if not _credentials_match_registered_user(username, password, registered_user):
            raise IncorrectCredentialsError()

        self._unlock_datastore_encryptor(username, password)

    def _unlock_datastore_encryptor(self, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        unlock_datastore_encryptor(self._data_dir, secret)

    def _reset_datastore_encryptor(self, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        reset_datastore_encryptor(self._data_dir, secret)


def _hash_password(plaintext_password: str) -> str:
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(plaintext_password.encode("utf-8"), salt)

    return password_hash.decode()


def _credentials_match_registered_user(
    username: str, password: str, registered_user: UserCreds
) -> bool:
    return (registered_user.username == username) and _password_matches_hash(
        password, registered_user.password_hash
    )


def _password_matches_hash(plaintext_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plaintext_password.encode("utf-8"), password_hash.encode("utf-8"))


def _get_secret_from_credentials(username: str, password: str) -> str:
    return f"{username}:{password}"
