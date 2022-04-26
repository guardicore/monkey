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
    DATA_DIR = None
    user_datastore = None

    # TODO: A number of these services should be instance objects instead of
    # static/singleton hybrids. At the moment, this requires invasive refactoring that's
    # not a priority.
    @classmethod
    def initialize(cls, data_dir: Path, user_datastore: IUserDatastore):
        cls.DATA_DIR = data_dir
        cls.user_datastore = user_datastore

    @classmethod
    def needs_registration(cls) -> bool:
        return not cls.user_datastore.has_registered_users()

    @classmethod
    def register_new_user(cls, username: str, password: str):
        if not username or not password:
            raise InvalidRegistrationCredentialsError("Username or password can not be empty.")

        credentials = UserCreds(username, _hash_password(password))
        cls.user_datastore.add_user(credentials)
        cls._reset_datastore_encryptor(username, password)
        reset_database()

    @classmethod
    def authenticate(cls, username: str, password: str):
        try:
            registered_user = cls.user_datastore.get_user_credentials(username)
        except UnknownUserError:
            raise IncorrectCredentialsError()

        if not _credentials_match_registered_user(username, password, registered_user):
            raise IncorrectCredentialsError()

        cls._unlock_datastore_encryptor(username, password)

    @classmethod
    def _unlock_datastore_encryptor(cls, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        unlock_datastore_encryptor(cls.DATA_DIR, secret)

    @classmethod
    def _reset_datastore_encryptor(cls, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        reset_datastore_encryptor(cls.DATA_DIR, secret)


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
