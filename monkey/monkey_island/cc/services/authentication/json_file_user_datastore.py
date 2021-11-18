import json
from pathlib import Path

from common.utils.exceptions import (
    AlreadyRegisteredError,
    InvalidRegistrationCredentialsError,
    UnknownUserError,
)
from monkey_island.cc.server_utils.file_utils import open_new_securely_permissioned_file

from .i_user_datastore import IUserDatastore
from .user_creds import UserCreds

CREDENTIALS_FILE = "credentials.json"


class JsonFileUserDatastore(IUserDatastore):
    def __init__(self, data_dir: Path):
        self._credentials = None
        self._credentials_file = data_dir / CREDENTIALS_FILE

        if self._credentials_file.exists():
            self._credentials = self._load_from_file()

    def _load_from_file(self) -> UserCreds:
        with open(self._credentials_file, "r") as f:
            credentials_dict = json.load(f)

            return UserCreds(credentials_dict["user"], credentials_dict["password_hash"])

    def has_registered_users(self) -> bool:
        return self._credentials is not None

    def add_user(self, credentials: UserCreds):
        if credentials is None:
            raise InvalidRegistrationCredentialsError("Credentials can not be 'None'")
        elif not credentials.username:
            raise InvalidRegistrationCredentialsError("Username can not be empty")
        elif not credentials.password_hash:
            raise InvalidRegistrationCredentialsError("Password hash can not be empty")

        if self._credentials:
            raise AlreadyRegisteredError(
                "User has already been registered. Reset credentials or login."
            )

        self._credentials = credentials
        self._store_credentials_to_file()

    def _store_credentials_to_file(self):
        with open_new_securely_permissioned_file(self._credentials_file, "w") as f:
            json.dump(self._credentials.to_dict(), f, indent=2)

    def get_user_credentials(self, username: str) -> UserCreds:
        if self._credentials is None or self._credentials.username != username:
            raise UnknownUserError(f"User {username} does not exist.")

        return self._credentials
