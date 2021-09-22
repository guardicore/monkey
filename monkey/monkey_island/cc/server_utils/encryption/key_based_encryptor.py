import base64
import logging

# PyCrypto is deprecated, but we use pycryptodome, which uses the exact same imports but
# is maintained.
from Crypto import Random  # noqa: DUO133  # nosec: B413
from Crypto.Cipher import AES  # noqa: DUO133  # nosec: B413

from monkey_island.cc.server_utils.encryption.i_encryptor import IEncryptor

logger = logging.getLogger(__name__)


class KeyBasedEncryptor(IEncryptor):

    _BLOCK_SIZE = 32

    def __init__(self, key: bytes):
        self._key = key

    def encrypt(self, plaintext: str) -> str:
        cipher_iv = Random.new().read(AES.block_size)
        cipher = AES.new(self._key, AES.MODE_CBC, cipher_iv)
        return base64.b64encode(cipher_iv + cipher.encrypt(self._pad(plaintext).encode())).decode()

    def decrypt(self, ciphertext: str):
        enc_message = base64.b64decode(ciphertext)
        cipher_iv = enc_message[0 : AES.block_size]
        cipher = AES.new(self._key, AES.MODE_CBC, cipher_iv)
        return self._unpad(cipher.decrypt(enc_message[AES.block_size :]).decode())

    def _pad(self, message):
        return message + (self._BLOCK_SIZE - (len(message) % self._BLOCK_SIZE)) * chr(
            self._BLOCK_SIZE - (len(message) % self._BLOCK_SIZE)
        )

    def _unpad(self, message: str):
        return message[0 : -ord(message[len(message) - 1])]
