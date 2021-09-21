from typing import List

from monkey_island.cc.models.utils.field_types.field_type_abc import FieldTypeABC
from monkey_island.cc.server_utils.encryption import string_encryptor


class StringList(FieldTypeABC):
    @staticmethod
    def encrypt(value: List[str]):
        return [string_encryptor.encrypt(string) for string in value]

    @staticmethod
    def decrypt(value: List[str]):
        return [string_encryptor.decrypt(string) for string in value]
