import os

# PyCrypto is deprecated, but we use pycryptodome, which uses the exact same imports but
# is maintained.
from Crypto import Random  # noqa: DUO133  # nosec: B413

from monkey_island.cc.server_utils.file_utils import open_new_securely_permissioned_file
from monkey_island.cc.services.utils.key_encryption import KeyBasedEncryptor

_encryptor = None


class DataStoreEncryptor:
    _BLOCK_SIZE = 32
    _PASSWORD_FILENAME = "mongo_key.bin"

    def __init__(self, password_file_dir):
        password_file = os.path.join(password_file_dir, self._PASSWORD_FILENAME)

        if os.path.exists(password_file):
            self._load_existing_key(password_file)
        else:
            self._init_key(password_file)

    def _init_key(self, password_file_path: str):
        self._cipher_key = Random.new().read(self._BLOCK_SIZE)
        with open_new_securely_permissioned_file(password_file_path, "wb") as f:
            f.write(self._cipher_key)

    def _load_existing_key(self, password_file):
        with open(password_file, "rb") as f:
            self._cipher_key = f.read()

    def enc(self, message: str):
        key_encryptor = KeyBasedEncryptor(self._cipher_key)
        return key_encryptor.encrypt(message)

    def dec(self, enc_message: str):
        key_encryptor = KeyBasedEncryptor(self._cipher_key)
        return key_encryptor.decrypt(enc_message)


def initialize_encryptor(password_file_dir):
    global _encryptor

    _encryptor = DataStoreEncryptor(password_file_dir)


def get_encryptor():
    return _encryptor
