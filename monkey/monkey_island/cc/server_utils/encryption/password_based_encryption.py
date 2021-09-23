import base64
import io
import logging

import pyAesCrypt

from monkey_island.cc.server_utils.encryption import IEncryptor

logger = logging.getLogger(__name__)

# PasswordBasedEncryptor as implemented takes low-entropy, user provided password and it adds some
# entropy to it and encrypts/decrypts the data. This implementation uses AES256-CBC
# and it is less secure encryption then KeyBasedEncryptor.
# The security of it depends on what will the user provide as password.
# We can merge the two into the one encryption method but then we lose the entropy
# of the key with whatever key derivation function we use.
# Note: password != key


class PasswordBasedEncryptor(IEncryptor):

    _BUFFER_SIZE = pyAesCrypt.crypto.bufferSizeDef

    def __init__(self, password: str):
        self.password = password

    def encrypt(self, plaintext: str) -> str:
        plaintext_stream = io.BytesIO(plaintext.encode())
        ciphertext_stream = io.BytesIO()

        pyAesCrypt.encryptStream(
            plaintext_stream, ciphertext_stream, self.password, self._BUFFER_SIZE
        )

        ciphertext_b64 = base64.b64encode(ciphertext_stream.getvalue())
        logger.info("String encrypted.")

        return ciphertext_b64.decode()

    def decrypt(self, ciphertext: str):
        ciphertext = base64.b64decode(ciphertext)
        ciphertext_stream = io.BytesIO(ciphertext)
        plaintext_stream = io.BytesIO()

        ciphertext_stream_len = len(ciphertext_stream.getvalue())

        try:
            pyAesCrypt.decryptStream(
                ciphertext_stream,
                plaintext_stream,
                self.password,
                self._BUFFER_SIZE,
                ciphertext_stream_len,
            )
        except ValueError as ex:
            if str(ex).startswith("Wrong password"):
                logger.info("Wrong password provided for decryption.")
                raise InvalidCredentialsError
            else:
                logger.info("The corrupt ciphertext provided.")
                raise InvalidCiphertextError
        return plaintext_stream.getvalue().decode("utf-8")


class InvalidCredentialsError(Exception):
    """ Raised when password for decryption is invalid """


class InvalidCiphertextError(Exception):
    """ Raised when ciphertext is corrupted """


def is_encrypted(ciphertext: str) -> bool:
    ciphertext = base64.b64decode(ciphertext)
    return ciphertext.startswith(b"AES")
