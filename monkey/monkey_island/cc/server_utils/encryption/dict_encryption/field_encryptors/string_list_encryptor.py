from typing import List

from monkey_island.cc.server_utils.encryption import get_datastore_encryptor
from monkey_island.cc.server_utils.encryption.dict_encryption.field_encryptors import (
    IFieldEncryptor,
)


class StringListEncryptor(IFieldEncryptor):
    @staticmethod
    def encrypt(value: List[str]):
        return [get_datastore_encryptor().enc(string) for string in value]

    @staticmethod
    def decrypt(value: List[str]):
        return [get_datastore_encryptor().dec(string) for string in value]
