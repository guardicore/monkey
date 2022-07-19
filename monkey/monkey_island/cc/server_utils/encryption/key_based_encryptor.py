import logging

from cryptography.fernet import Fernet

from .i_encryptor import IEncryptor

logger = logging.getLogger(__name__)

# KeyBasedEncryptor is an encryption method which use random key of specific length
# and AES block cipher to encrypt/decrypt the data. The key is more complex
# one and hard to remember than user provided one. This class provides more secure way of
# encryption compared to PasswordBasedEncryptor because of the random and complex key.
# We can merge the two into the one encryption method but then we lose the entropy
# of the key with whatever key derivation function we use.
# Note: password != key


class SizeError(Exception):
    """
    Raised when an argument is not of the expected size during object creation.
    """

    pass


class EncryptionKey32Bit(bytes):
    def __init__(self, key: bytes):
        if len(key) == 32:
            self.key = key
        else:
            raise SizeError("Key size should be 32 bytes.")


class KeyBasedEncryptor(IEncryptor):
    def __init__(self, key: bytes):
        """
        Initializes a KeyBasedEncryptor object
        :param bytes key: The encryption key with which the object should be initialized.
                          This should be a URL-safe base64-encoded 32-byte key.
        """
        self._key = key
        self._fernet_object = Fernet(self._key)

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
