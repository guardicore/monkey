from monkey_island.cc.server_utils.encryption import (
    reset_datastore_encryptor,
    unlock_datastore_encryptor,
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
    def unlock_datastore_encryptor(username: str, password: str):
        secret = AuthenticationService._get_secret_from_credentials(username, password)
        unlock_datastore_encryptor(AuthenticationService.KEY_FILE_DIRECTORY, secret)

    @staticmethod
    def reset_datastore_encryptor(username: str, password: str):
        secret = AuthenticationService._get_secret_from_credentials(username, password)
        reset_datastore_encryptor(AuthenticationService.KEY_FILE_DIRECTORY, secret)

    @staticmethod
    def _get_secret_from_credentials(username: str, password: str) -> str:
        return f"{username}:{password}"
