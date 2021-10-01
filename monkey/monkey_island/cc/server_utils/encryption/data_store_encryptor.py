from __future__ import annotations

import os

# PyCrypto is deprecated, but we use pycryptodome, which uses the exact same imports but
# is maintained.
from typing import Union

from Crypto import Random  # noqa: DUO133  # nosec: B413

from monkey_island.cc.server_utils.encryption import FactoryNotInitializedError, KeyBasedEncryptor
from monkey_island.cc.server_utils.encryption.encryptor_factory import (
    get_encryptor_factory,
    get_secret_from_credentials,
)
from monkey_island.cc.server_utils.encryption.password_based_bytes_encryption import (
    PasswordBasedBytesEncryptor,
)
from monkey_island.cc.server_utils.file_utils import open_new_securely_permissioned_file

_encryptor: Union[None, DataStoreEncryptor] = None


class DataStoreEncryptor:
    _BLOCK_SIZE = 32

    def __init__(self, key_file_path: str, secret: str):
        if os.path.exists(key_file_path):
            self._key_based_encryptor = DataStoreEncryptor._load_existing_key(key_file_path, secret)
        else:
            self._key_based_encryptor = DataStoreEncryptor._create_new_key(key_file_path, secret)

    @staticmethod
    def _load_existing_key(key_file_path: str, secret: str):
        with open(key_file_path, "rb") as f:
            encrypted_key = f.read()
        cipher_key = PasswordBasedBytesEncryptor(secret).decrypt(encrypted_key)
        return KeyBasedEncryptor(cipher_key)

    @staticmethod
    def _create_new_key(key_file_path: str, secret: str):
        cipher_key = Random.new().read(DataStoreEncryptor._BLOCK_SIZE)
        encrypted_key = PasswordBasedBytesEncryptor(secret).encrypt(cipher_key)
        with open_new_securely_permissioned_file(key_file_path, "wb") as f:
            f.write(encrypted_key)
        return KeyBasedEncryptor(cipher_key)

    def enc(self, message: str):
        return self._key_based_encryptor.encrypt(message)

    def dec(self, enc_message: str):
        return self._key_based_encryptor.decrypt(enc_message)


def initialize_datastore_encryptor(username: str, password: str):
    global _encryptor

    factory = get_encryptor_factory()
    if not factory:
        raise FactoryNotInitializedError
    secret = get_secret_from_credentials(username, password)
    _encryptor = DataStoreEncryptor(factory.key_file_path, secret)


def get_datastore_encryptor():
    return _encryptor
