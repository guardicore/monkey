import base64
import logging

import pyAesCrypt

from monkey_island.cc.server_utils.encryption import IEncryptor
from monkey_island.cc.server_utils.encryption.password_based_bytes_encryption import (
    PasswordBasedBytesEncryptor,
)

logger = logging.getLogger(__name__)


class PasswordBasedStringEncryptor(IEncryptor):

    _BUFFER_SIZE = pyAesCrypt.crypto.bufferSizeDef

    def __init__(self, password: str):
        self.password = password

    def encrypt(self, plaintext: str) -> str:
        ciphertext = PasswordBasedBytesEncryptor(self.password).encrypt(plaintext.encode())

        return base64.b64encode(ciphertext).decode()

    def decrypt(self, ciphertext: str) -> str:
        ciphertext = base64.b64decode(ciphertext)

        plaintext_stream = PasswordBasedBytesEncryptor(self.password).decrypt(ciphertext)
        return plaintext_stream.decode()


def is_encrypted(ciphertext: str) -> bool:
    ciphertext = base64.b64decode(ciphertext)
    return ciphertext.startswith(b"AES")
