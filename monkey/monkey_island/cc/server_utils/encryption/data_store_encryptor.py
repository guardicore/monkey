import os
from pathlib import Path
from typing import Union

from cryptography.fernet import Fernet

from monkey_island.cc.server_utils.file_utils import open_new_securely_permissioned_file

from .i_encryptor import IEncryptor
from .key_based_encryptor import KeyBasedEncryptor
from .password_based_bytes_encryptor import PasswordBasedBytesEncryptor

_KEY_FILE_NAME = "mongo_key.bin"

_encryptor: Union[None, IEncryptor] = None


# NOTE: This class is being replaced by RepositoryEncryptor
class DataStoreEncryptor(IEncryptor):
    def __init__(self, secret: str, key_file: Path):
        self._key_file = key_file
        self._password_based_encryptor = PasswordBasedBytesEncryptor(secret)
        self._key_based_encryptor = self._initialize_key_based_encryptor()

    def _initialize_key_based_encryptor(self):
        if os.path.exists(self._key_file):
            return self._load_key()

        return self._create_key()

    def _load_key(self) -> KeyBasedEncryptor:
        with open(self._key_file, "rb") as f:
            encrypted_key = f.read()

        plaintext_key = self._password_based_encryptor.decrypt(encrypted_key)
        return KeyBasedEncryptor(plaintext_key)

    def _create_key(self) -> KeyBasedEncryptor:
        plaintext_key = Fernet.generate_key()

        encrypted_key = self._password_based_encryptor.encrypt(plaintext_key)
        with open_new_securely_permissioned_file(str(self._key_file), "wb") as f:
            f.write(encrypted_key)

        return KeyBasedEncryptor(plaintext_key)

    def encrypt(self, plaintext: bytes) -> bytes:
        return self._key_based_encryptor.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self._key_based_encryptor.decrypt(ciphertext)


def reset_datastore_encryptor(key_file_dir: Path, secret: str, key_file_name: str = _KEY_FILE_NAME):
    key_file = key_file_dir / key_file_name

    if key_file.is_file():
        key_file.unlink()

    _initialize_datastore_encryptor(key_file, secret)


def unlock_datastore_encryptor(
    key_file_dir: Path, secret: str, key_file_name: str = _KEY_FILE_NAME
):
    key_file = key_file_dir / key_file_name
    _initialize_datastore_encryptor(key_file, secret)


def _initialize_datastore_encryptor(key_file: Path, secret: str):
    global _encryptor

    _encryptor = DataStoreEncryptor(secret, key_file)


def get_datastore_encryptor() -> IEncryptor:
    return _encryptor
