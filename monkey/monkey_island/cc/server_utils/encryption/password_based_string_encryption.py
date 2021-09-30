import base64
import io
import logging

import pyAesCrypt

from monkey_island.cc.server_utils.encryption import IEncryptor
from monkey_island.cc.server_utils.encryption.password_based_byte_encryption import (
    PasswordBasedByteEncryptor,
)

logger = logging.getLogger(__name__)


class PasswordBasedStringEncryptor(IEncryptor):

    _BUFFER_SIZE = pyAesCrypt.crypto.bufferSizeDef

    def __init__(self, password: str):
        self.password = password

    def encrypt(self, plaintext: str) -> str:
        plaintext_stream = io.BytesIO(plaintext.encode())
        ciphertext = PasswordBasedByteEncryptor(self.password).encrypt(plaintext_stream)

        return base64.b64encode(ciphertext.getvalue()).decode()

    def decrypt(self, ciphertext: str) -> str:
        ciphertext = base64.b64decode(ciphertext)
        ciphertext_stream = io.BytesIO(ciphertext)

        plaintext_stream = PasswordBasedByteEncryptor(self.password).decrypt(ciphertext_stream)
        return plaintext_stream.getvalue().decode("utf-8")


def is_encrypted(ciphertext: str) -> bool:
    ciphertext = base64.b64decode(ciphertext)
    return ciphertext.startswith(b"AES")
