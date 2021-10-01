from __future__ import annotations

# PyCrypto is deprecated, but we use pycryptodome, which uses the exact same imports but
# is maintained.
from typing import Union

from monkey_island.cc.server_utils.encryption import KeyBasedEncryptor

_encryptor: Union[None, DataStoreEncryptor] = None


class DataStoreEncryptor:
    def __init__(self, key_based_encryptor: KeyBasedEncryptor):
        self._key_based_encryptor = key_based_encryptor

    def enc(self, message: str):
        return self._key_based_encryptor.encrypt(message)

    def dec(self, enc_message: str):
        return self._key_based_encryptor.decrypt(enc_message)


def initialize_datastore_encryptor(key_based_encryptor: KeyBasedEncryptor):
    global _encryptor

    _encryptor = DataStoreEncryptor(key_based_encryptor)


def get_datastore_encryptor():
    return _encryptor
