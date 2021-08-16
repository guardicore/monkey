import base64
import io
import logging

import pyAesCrypt

BUFFER_SIZE = pyAesCrypt.crypto.bufferSizeDef

logger = logging.getLogger(__name__)


def encrypt_string(plaintext: str, password: str) -> str:
    plaintext_stream = io.BytesIO(plaintext.encode())
    ciphertext_stream = io.BytesIO()

    pyAesCrypt.encryptStream(plaintext_stream, ciphertext_stream, password, BUFFER_SIZE)

    ciphertext_b64 = base64.b64encode(ciphertext_stream.getvalue())
    logger.info("String encrypted.")

    return ciphertext_b64.decode()


def decrypt_ciphertext(ciphertext: str, password: str) -> str:
    ciphertext = base64.b64decode(ciphertext)
    ciphertext_stream = io.BytesIO(ciphertext)
    plaintext_stream = io.BytesIO()

    ciphertext_stream_len = len(ciphertext_stream.getvalue())

    try:
        pyAesCrypt.decryptStream(
            ciphertext_stream,
            plaintext_stream,
            password,
            BUFFER_SIZE,
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


def is_encrypted(ciphertext: str) -> bool:
    ciphertext = base64.b64decode(ciphertext)
    return ciphertext.startswith(b"AES")


class InvalidCredentialsError(Exception):
    """ Raised when password for decryption is invalid """


class InvalidCiphertextError(Exception):
    """ Raised when ciphertext is corrupted """
