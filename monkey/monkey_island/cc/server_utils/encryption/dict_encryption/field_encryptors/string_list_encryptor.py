from typing import List

from ... import get_datastore_encryptor
from . import IFieldEncryptor


class StringListEncryptor(IFieldEncryptor):
    @staticmethod
    def encrypt(value: List[str]):
        return [get_datastore_encryptor().encrypt(string) for string in value]

    @staticmethod
    def decrypt(value: List[str]):
        return [get_datastore_encryptor().decrypt(string) for string in value]
