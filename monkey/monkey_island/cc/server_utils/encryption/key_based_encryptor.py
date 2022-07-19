import base64
import logging

from cryptography.fernet import Fernet

from . import EncryptionKey32Bytes
from .i_encryptor import IEncryptor

logger = logging.getLogger(__name__)

# KeyBasedEncryptor is an encryption method which use random key of specific length
# and AES block cipher to encrypt/decrypt the data. The key is more complex
# one and hard to remember than user provided one. This class provides more secure way of
# encryption compared to PasswordBasedEncryptor because of the random and complex key.
# We can merge the two into the one encryption method but then we lose the entropy
# of the key with whatever key derivation function we use.
# Note: password != key


class KeyBasedEncryptor(IEncryptor):
    def __init__(self, key: EncryptionKey32Bytes):
        """
        Initializes a KeyBasedEncryptor object
        :param EncryptionKey32Bytes key: The encryption key with which the object should be
                                         initialized.
        """
        self._formatted_key = base64.urlsafe_b64encode(key)
        self._fernet_object = Fernet(self._formatted_key)

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypts a given bytestream
        :param bytes plaintext: The bytestream to encrypt
        :return: Encrypted message
        :rtype: bytes
        """
        return self._fernet_object.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypts a given bytestream
        :param bytes ciphertext: The bytestream to decrypt
        :return: Decrypted message
        :rtype: bytes
        """
        return self._fernet_object.decrypt(ciphertext)
