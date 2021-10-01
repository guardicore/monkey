from __future__ import annotations

import os
from ctypes import Union

_factory: Union[None, EncryptorFactory] = None


class EncryptorFactory:

    _KEY_FILENAME = "mongo_key.bin"

    def __init__(self, key_file_dir: str):
        self.key_file_path = os.path.join(key_file_dir, self._KEY_FILENAME)


class FactoryNotInitializedError(Exception):
    pass


def get_secret_from_credentials(username: str, password: str) -> str:
    return f"{username}:{password}"


def remove_old_datastore_key():
    if _factory is None:
        raise FactoryNotInitializedError
    if os.path.isfile(_factory.key_file_path):
        os.remove(_factory.key_file_path)


def initialize_encryptor_factory(key_file_dir: str):
    global _factory
    _factory = EncryptorFactory(key_file_dir)


def get_encryptor_factory():
    return _factory
