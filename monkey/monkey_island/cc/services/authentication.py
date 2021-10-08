import bcrypt

import monkey_island.cc.environment.environment_singleton as env_singleton
from monkey_island.cc.environment.user_creds import UserCreds
from monkey_island.cc.resources.auth.credential_utils import password_matches_hash
from monkey_island.cc.server_utils.encryption import (
    reset_datastore_encryptor,
    unlock_datastore_encryptor,
)
from monkey_island.cc.setup.mongo.database_initializer import reset_database


class AuthenticationService:
    KEY_FILE_DIRECTORY = None

    # TODO: A number of these services should be instance objects instead of
    # static/singleton hybrids. At the moment, this requires invasive refactoring that's
    # not a priority.
    @classmethod
    def initialize(cls, key_file_directory):
        cls.KEY_FILE_DIRECTORY = key_file_directory

    @staticmethod
    def needs_registration() -> bool:
        return env_singleton.env.needs_registration()

    @classmethod
    def register_new_user(cls, username: str, password: str):
        credentials = UserCreds(username, _hash_password(password))
        env_singleton.env.try_add_user(credentials)
        cls._reset_datastore_encryptor(username, password)
        reset_database()

    @classmethod
    def authenticate(cls, username: str, password: str) -> bool:
        if _credentials_match_registered_user(username, password):
            cls._unlock_datastore_encryptor(username, password)
            return True

        return False

    @classmethod
    def _unlock_datastore_encryptor(cls, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        unlock_datastore_encryptor(cls.KEY_FILE_DIRECTORY, secret)

    @classmethod
    def _reset_datastore_encryptor(cls, username: str, password: str):
        secret = _get_secret_from_credentials(username, password)
        reset_datastore_encryptor(cls.KEY_FILE_DIRECTORY, secret)


def _hash_password(plaintext_password):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(plaintext_password.encode("utf-8"), salt)

    return password_hash.decode()


def _credentials_match_registered_user(username: str, password: str) -> bool:
    registered_user = env_singleton.env.get_user()

    if not registered_user:
        return False

    return (registered_user.username == username) and password_matches_hash(
        password, registered_user.password_hash
    )


def _get_secret_from_credentials(username: str, password: str) -> str:
    return f"{username}:{password}"
