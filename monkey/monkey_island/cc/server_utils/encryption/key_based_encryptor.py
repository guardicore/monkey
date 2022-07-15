import base64
import logging

# PyCrypto is deprecated, but we use pycryptodome, which uses the exact same imports but
# is maintained.
from Crypto import Random  # noqa: DUO133  # nosec: B413
from Crypto.Cipher import AES  # noqa: DUO133  # nosec: B413
from Crypto.Util import Padding  # noqa: DUO133

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

    _BLOCK_SIZE = 32

    def __init__(self, key: bytes):
        self._key = key

    def encrypt(self, plaintext: bytes) -> bytes:
        cipher_iv = Random.new().read(AES.block_size)
        cipher = AES.new(self._key, AES.MODE_CBC, cipher_iv)
        padded_plaintext = Padding.pad(plaintext, self._BLOCK_SIZE)
        return base64.b64encode(cipher_iv + cipher.encrypt(padded_plaintext))

    def decrypt(self, ciphertext: bytes) -> bytes:
        enc_message = base64.b64decode(ciphertext)
        cipher_iv = enc_message[0 : AES.block_size]
        cipher = AES.new(self._key, AES.MODE_CBC, cipher_iv)
        padded_plaintext = cipher.decrypt(enc_message[AES.block_size :])
        return Padding.unpad(padded_plaintext, self._BLOCK_SIZE)
