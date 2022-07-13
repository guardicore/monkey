from typing import List

from ..data_store_encryptor import get_datastore_encryptor
from . import IFieldEncryptor


class StringListEncryptor(IFieldEncryptor):
    @staticmethod
    def encrypt(value: List[str]) -> List[str]:
        return [get_datastore_encryptor().encrypt(string.encode()).decode() for string in value]

    @staticmethod
    def decrypt(value: List[str]) -> List[str]:
        return [get_datastore_encryptor().decrypt(string.encode()).decode() for string in value]
