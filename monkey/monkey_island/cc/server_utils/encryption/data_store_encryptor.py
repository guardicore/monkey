import io
import os

# PyCrypto is deprecated, but we use pycryptodome, which uses the exact same imports but
# is maintained.
from Crypto import Random  # noqa: DUO133  # nosec: B413

from monkey_island.cc.server_utils.encryption import KeyBasedEncryptor
from monkey_island.cc.server_utils.encryption.password_based_byte_encryption import (
    PasswordBasedByteEncryptor,
)
from monkey_island.cc.server_utils.file_utils import open_new_securely_permissioned_file

_encryptor = None


class DataStoreEncryptor:
    _BLOCK_SIZE = 32
    _KEY_FILENAME = "mongo_key.bin"

    def __init__(self, key_file_dir: str, secret: str):
        key_file = os.path.join(key_file_dir, self._KEY_FILENAME)

        if os.path.exists(key_file):
            self._load_existing_key(key_file, secret)
        else:
            self._init_key(key_file, secret)

        self._key_base_encryptor = KeyBasedEncryptor(self._cipher_key)

    def _init_key(self, password_file_path: str, secret: str):
        self._cipher_key = Random.new().read(self._BLOCK_SIZE)
        encrypted_key = (
            PasswordBasedByteEncryptor(secret).encrypt(io.BytesIO(self._cipher_key)).getvalue()
        )
        with open_new_securely_permissioned_file(password_file_path, "wb") as f:
            f.write(encrypted_key)

    def _load_existing_key(self, key_file_path: str, secret: str):
        with open(key_file_path, "rb") as f:
            encrypted_key = f.read()
        self._cipher_key = (
            PasswordBasedByteEncryptor(secret).decrypt(io.BytesIO(encrypted_key)).getvalue()
        )

    def enc(self, message: str):
        return self._key_base_encryptor.encrypt(message)

    def dec(self, enc_message: str):
        return self._key_base_encryptor.decrypt(enc_message)


def initialize_datastore_encryptor(key_file_dir: str, secret: str):
    global _encryptor

    _encryptor = DataStoreEncryptor(key_file_dir, secret)


def get_datastore_encryptor():
    return _encryptor
