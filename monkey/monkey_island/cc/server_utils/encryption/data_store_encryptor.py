import os

# PyCrypto is deprecated, but we use pycryptodome, which uses the exact same imports but
# is maintained.
from Crypto import Random  # noqa: DUO133  # nosec: B413

from monkey_island.cc.server_utils.encryption import KeyBasedEncryptor
from monkey_island.cc.server_utils.file_utils import open_new_securely_permissioned_file

_encryptor = None


class DataStoreEncryptor:
    _BLOCK_SIZE = 32
    _KEY_FILENAME = "mongo_key.bin"

    def __init__(self, key_file_dir):
        key_file = os.path.join(key_file_dir, self._KEY_FILENAME)

        if os.path.exists(key_file):
            self._load_existing_key(key_file)
        else:
            self._init_key(key_file)

        self._key_base_encryptor = KeyBasedEncryptor(self._cipher_key)

    def _init_key(self, password_file_path: str):
        self._cipher_key = Random.new().read(self._BLOCK_SIZE)
        with open_new_securely_permissioned_file(password_file_path, "wb") as f:
            f.write(self._cipher_key)

    def _load_existing_key(self, key_file):
        with open(key_file, "rb") as f:
            self._cipher_key = f.read()

    def enc(self, message: str):
        return self._key_base_encryptor.encrypt(message)

    def dec(self, enc_message: str):
        return self._key_base_encryptor.decrypt(enc_message)


def initialize_encryptor(key_file_dir):
    global _encryptor

    _encryptor = DataStoreEncryptor(key_file_dir)


def get_encryptor():
    return _encryptor
