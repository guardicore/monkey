from ..data_store_encryptor import get_datastore_encryptor
from . import IFieldEncryptor


class StringEncryptor(IFieldEncryptor):
    @staticmethod
    def encrypt(value: str):
        return get_datastore_encryptor().encrypt(value)

    @staticmethod
    def decrypt(value: str):
        return get_datastore_encryptor().decrypt(value)
