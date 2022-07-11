from typing import List

from ..data_store_encryptor import get_datastore_encryptor
from . import IFieldEncryptor


class StringListEncryptor(IFieldEncryptor):
    @staticmethod
    def encrypt(value: List[str]):
        return [get_datastore_encryptor().encrypt(string.encode()) for string in value]

    @staticmethod
    def decrypt(value: List[bytes]):
        return [get_datastore_encryptor().decrypt(bytes_).decode() for bytes_ in value]
