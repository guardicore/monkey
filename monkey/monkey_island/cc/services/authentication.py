from monkey_island.cc.server_utils.encryption import (
    get_datastore_encryptor,
    initialize_datastore_encryptor,
    remove_old_datastore_key,
)


class AuthenticationService:
    KEY_FILE_DIRECTORY = None

    # TODO: A number of these services should be instance objects instead of
    # static/singleton hybrids. At the moment, this requires invasive refactoring that's
    # not a priority.
    @classmethod
    def initialize(cls, key_file_directory):
        cls.KEY_FILE_DIRECTORY = key_file_directory

    @staticmethod
    def ensure_datastore_encryptor(username: str, password: str):
        if not get_datastore_encryptor():
            AuthenticationService._init_encryptor_from_credentials(username, password)

    @staticmethod
    def reset_datastore_encryptor(username: str, password: str):
        remove_old_datastore_key(AuthenticationService.KEY_FILE_DIRECTORY)
        AuthenticationService._init_encryptor_from_credentials(username, password)

    @staticmethod
    def _init_encryptor_from_credentials(username: str, password: str):
        secret = AuthenticationService._get_secret_from_credentials(username, password)
        initialize_datastore_encryptor(AuthenticationService.KEY_FILE_DIRECTORY, secret)

    @staticmethod
    def _get_secret_from_credentials(username: str, password: str) -> str:
        return f"{username}:{password}"
