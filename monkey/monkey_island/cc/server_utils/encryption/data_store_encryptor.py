import os
from typing import Union

from Crypto import Random  # noqa: DUO133  # nosec: B413

from monkey_island.cc.server_utils.encryption import IEncryptor, KeyBasedEncryptor
from monkey_island.cc.server_utils.encryption.encryptors.password_based_bytes_encryption import (
    PasswordBasedBytesEncryptor,
)
from monkey_island.cc.server_utils.file_utils import open_new_securely_permissioned_file

_KEY_FILENAME = "mongo_key.bin"
_BLOCK_SIZE = 32

_encryptor: Union[None, IEncryptor] = None


def _load_existing_key(key_file_path: str, secret: str) -> KeyBasedEncryptor:
    with open(key_file_path, "rb") as f:
        encrypted_key = f.read()
    cipher_key = PasswordBasedBytesEncryptor(secret).decrypt(encrypted_key)
    return KeyBasedEncryptor(cipher_key)


def _create_new_key(key_file_path: str, secret: str) -> KeyBasedEncryptor:
    cipher_key = _get_random_bytes()
    encrypted_key = PasswordBasedBytesEncryptor(secret).encrypt(cipher_key)
    with open_new_securely_permissioned_file(key_file_path, "wb") as f:
        f.write(encrypted_key)
    return KeyBasedEncryptor(cipher_key)


def _get_random_bytes() -> bytes:
    return Random.new().read(_BLOCK_SIZE)


def remove_old_datastore_key(key_file_dir: str):
    key_file_path = _get_key_file_path(key_file_dir)
    if os.path.isfile(key_file_path):
        os.remove(key_file_path)


def initialize_datastore_encryptor(key_file_dir: str, secret: str):
    global _encryptor

    key_file_path = _get_key_file_path(key_file_dir)
    if os.path.exists(key_file_path):
        _encryptor = _load_existing_key(key_file_path, secret)
    else:
        _encryptor = _create_new_key(key_file_path, secret)


def _get_key_file_path(key_file_dir: str) -> str:
    return os.path.join(key_file_dir, _KEY_FILENAME)


def get_datastore_encryptor() -> IEncryptor:
    return _encryptor
