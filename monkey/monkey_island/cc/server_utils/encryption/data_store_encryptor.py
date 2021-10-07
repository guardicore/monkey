import os
from pathlib import Path
from typing import Union

from Crypto import Random  # noqa: DUO133  # nosec: B413

from monkey_island.cc.server_utils.file_utils import open_new_securely_permissioned_file

from .i_encryptor import IEncryptor
from .key_based_encryptor import KeyBasedEncryptor
from .password_based_bytes_encryptor import PasswordBasedBytesEncryptor

_encryptor: Union[None, IEncryptor] = None


class DataStoreEncryptor(IEncryptor):
    _KEY_LENGTH_BYTES = 32

    def __init__(self, secret: str, key_file_path: Path):
        self._key_file_path = key_file_path
        self._password_based_encryptor = PasswordBasedBytesEncryptor(secret)
        self._key_based_encryptor = self._initialize_key_based_encryptor()

    def _initialize_key_based_encryptor(self):
        if os.path.exists(self._key_file_path):
            return self._load_existing_key()

        return self._create_new_key()

    def _load_existing_key(self) -> KeyBasedEncryptor:
        with open(self._key_file_path, "rb") as f:
            encrypted_key = f.read()

        plaintext_key = self._password_based_encryptor.decrypt(encrypted_key)
        return KeyBasedEncryptor(plaintext_key)

    def _create_new_key(self) -> KeyBasedEncryptor:
        plaintext_key = Random.new().read(DataStoreEncryptor._KEY_LENGTH_BYTES)

        encrypted_key = self._password_based_encryptor.encrypt(plaintext_key)
        with open_new_securely_permissioned_file(self._key_file_path, "wb") as f:
            f.write(encrypted_key)

        return KeyBasedEncryptor(plaintext_key)

    def encrypt(self, plaintext: str) -> str:
        return self._key_based_encryptor.encrypt(plaintext)

    def decrypt(self, ciphertext: str):
        return self._key_based_encryptor.decrypt(ciphertext)


def reset_datastore_encryptor(key_file_dir: str, secret: str, key_file_name: str = "mongo_key.bin"):
    key_file_path = Path(key_file_dir) / key_file_name

    if key_file_path.is_file():
        key_file_path.unlink()

    unlock_datastore_encryptor(key_file_dir, secret, key_file_name)


def unlock_datastore_encryptor(
    key_file_dir: str, secret: str, key_file_name: str = "mongo_key.bin"
):
    global _encryptor

    key_file_path = Path(key_file_dir) / key_file_name
    _encryptor = DataStoreEncryptor(secret, key_file_path)


def get_datastore_encryptor() -> IEncryptor:
    return _encryptor
