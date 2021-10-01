import os

from Crypto import Random

from monkey_island.cc.server_utils.encryption import (
    KeyBasedEncryptor,
    initialize_datastore_encryptor,
)
from monkey_island.cc.server_utils.encryption.password_based_bytes_encryption import (
    PasswordBasedBytesEncryptor,
)
from monkey_island.cc.server_utils.file_utils import open_new_securely_permissioned_file

_KEY_FILENAME = "mongo_key.bin"
_BLOCK_SIZE = 32


class EncryptorFactory:
    def __init__(self):
        self.key_file_path = None
        self.secret = None

    def set_key_file_path(self, key_file_path: str):
        self.key_file_path = key_file_path

    def set_secret(self, username: str, password: str):
        self.secret = _get_secret_from_credentials(username, password)

    def initialize_encryptor(self):
        if os.path.exists(self.key_file_path):
            key_based_encryptor = _load_existing_key(self.key_file_path, self.secret)
        else:
            key_based_encryptor = _create_new_key(self.key_file_path, self.secret)
        initialize_datastore_encryptor(key_based_encryptor)


class KeyPathNotSpecifiedError(Exception):
    pass


def _load_existing_key(key_file_path: str, secret: str):
    with open(key_file_path, "rb") as f:
        encrypted_key = f.read()
    cipher_key = PasswordBasedBytesEncryptor(secret).decrypt(encrypted_key)
    return KeyBasedEncryptor(cipher_key)


def _create_new_key(key_file_path: str, secret: str):
    cipher_key = _get_random_bytes()
    encrypted_key = PasswordBasedBytesEncryptor(secret).encrypt(cipher_key)
    with open_new_securely_permissioned_file(key_file_path, "wb") as f:
        f.write(encrypted_key)
    return KeyBasedEncryptor(cipher_key)


def _get_random_bytes() -> bytes:
    return Random.new().read(_BLOCK_SIZE)


def _get_secret_from_credentials(username: str, password: str) -> str:
    return f"{username}:{password}"


def remove_old_datastore_key():
    if not _factory.key_file_path:
        raise KeyPathNotSpecifiedError
    if os.path.isfile(_factory.key_file_path):
        os.remove(_factory.key_file_path)


def get_encryptor_factory():
    return _factory


_factory = EncryptorFactory()
