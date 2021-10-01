from __future__ import annotations

import io
import os

# PyCrypto is deprecated, but we use pycryptodome, which uses the exact same imports but
# is maintained.
from typing import Union

from Crypto import Random  # noqa: DUO133  # nosec: B413

from monkey_island.cc.server_utils.encryption import KeyBasedEncryptor
from monkey_island.cc.server_utils.encryption.password_based_byte_encryption import (
    PasswordBasedByteEncryptor,
)
from monkey_island.cc.server_utils.file_utils import open_new_securely_permissioned_file

_encryptor: Union[None, DataStoreEncryptor] = None


class DataStoreEncryptor:
    _BLOCK_SIZE = 32
    _KEY_FILENAME = "mongo_key.bin"

    def __init__(self, key_file_dir: str):
        self.key_file_path = os.path.join(key_file_dir, self._KEY_FILENAME)
        self._key_base_encryptor = None

    def init_key(self, secret: str):
        if os.path.exists(self.key_file_path):
            self._load_existing_key(secret)
        else:
            self._create_new_key(secret)

    def _load_existing_key(self, secret: str):
        with open(self.key_file_path, "rb") as f:
            encrypted_key = f.read()
        cipher_key = (
            PasswordBasedByteEncryptor(secret).decrypt(io.BytesIO(encrypted_key)).getvalue()
        )
        self._key_base_encryptor = KeyBasedEncryptor(cipher_key)

    def _create_new_key(self, secret: str):
        cipher_key = Random.new().read(self._BLOCK_SIZE)
        encrypted_key = (
            PasswordBasedByteEncryptor(secret).encrypt(io.BytesIO(cipher_key)).getvalue()
        )
        with open_new_securely_permissioned_file(self.key_file_path, "wb") as f:
            f.write(encrypted_key)
        self._key_base_encryptor = KeyBasedEncryptor(cipher_key)

    def is_key_setup(self) -> bool:
        return self._key_base_encryptor is not None

    def enc(self, message: str):
        return self._key_base_encryptor.encrypt(message)

    def dec(self, enc_message: str):
        return self._key_base_encryptor.decrypt(enc_message)


def initialize_datastore_encryptor(key_file_dir: str):
    global _encryptor

    _encryptor = DataStoreEncryptor(key_file_dir)


class EncryptorNotInitializedError(Exception):
    pass


def _get_secret_from_credentials(username: str, password: str) -> str:
    return f"{username}:{password}"


def encryptor_initialized_key_not_set(f):
    def inner_function(*args, **kwargs):
        if _encryptor is None:
            raise EncryptorNotInitializedError
        else:
            if not _encryptor.is_key_setup():
                return f(*args, **kwargs)
            else:
                pass

    return inner_function


@encryptor_initialized_key_not_set
def remove_old_datastore_key():
    if os.path.isfile(_encryptor.key_file_path):
        os.remove(_encryptor.key_file_path)


@encryptor_initialized_key_not_set
def setup_datastore_key(username: str, password: str):
    secret = _get_secret_from_credentials(username, password)
    _encryptor.init_key(secret)


def get_datastore_encryptor():
    return _encryptor
