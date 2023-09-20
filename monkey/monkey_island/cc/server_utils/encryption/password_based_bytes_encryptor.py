import io
import logging

import pyAesCrypt

from .i_encryptor import IEncryptor

logger = logging.getLogger(__name__)

# PasswordBasedEncryptor as implemented takes low-entropy, user provided password and it adds some
# entropy to it and encrypts/decrypts the data. This implementation uses AES256-CBC
# and it is less secure encryption then KeyBasedEncryptor.
# The security of it depends on what will the user provide as password.
# We can merge the two into the one encryption method but then we lose the entropy
# of the key with whatever key derivation function we use.
# Note: password != key


class PasswordBasedBytesEncryptor(IEncryptor):
    _BUFFER_SIZE = pyAesCrypt.crypto.bufferSizeDef

    def __init__(self, password: str):
        self.password = password

    def encrypt(self, plaintext: bytes) -> bytes:
        ciphertext_stream = io.BytesIO()

        pyAesCrypt.encryptStream(
            io.BytesIO(plaintext), ciphertext_stream, self.password, self._BUFFER_SIZE
        )

        return ciphertext_stream.getvalue()

    def decrypt(self, ciphertext: bytes) -> bytes:
        plaintext_stream = io.BytesIO()

        ciphertext_stream_len = len(ciphertext)

        try:
            pyAesCrypt.decryptStream(
                io.BytesIO(ciphertext),
                plaintext_stream,
                self.password,
                self._BUFFER_SIZE,
                ciphertext_stream_len,
            )
        except ValueError as ex:
            if str(ex).startswith("Wrong password"):
                logger.debug("Wrong password provided for decryption.")
                raise InvalidCredentialsError
            else:
                logger.error("The provided ciphertext was corrupt.")
                raise InvalidCiphertextError
        return plaintext_stream.getvalue()


class InvalidCredentialsError(Exception):
    """Raised when password for decryption is invalid"""


class InvalidCiphertextError(Exception):
    """Raised when ciphertext is corrupted"""
