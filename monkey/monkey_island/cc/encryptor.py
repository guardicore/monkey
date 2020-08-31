import base64
import os

# PyCrypto is deprecated, but we use pycryptodome, which uses the exact same imports but it maintained
from Crypto import Random  # noqa: DOU133
from Crypto.Cipher import AES  # noqa: DOU133

from monkey_island.cc.consts import MONKEY_ISLAND_ABS_PATH

__author__ = "itay.mizeretz"


class Encryptor:
    _BLOCK_SIZE = 32
    _DB_PASSWORD_FILENAME = os.path.join(MONKEY_ISLAND_ABS_PATH, 'cc/mongo_key.bin')

    def __init__(self):
        self._load_key()

    def _init_key(self):
        self._cipher_key = Random.new().read(self._BLOCK_SIZE)
        with open(self._DB_PASSWORD_FILENAME, 'wb') as f:
            f.write(self._cipher_key)

    def _load_existing_key(self):
        with open(self._DB_PASSWORD_FILENAME, 'rb') as f:
            self._cipher_key = f.read()

    def _load_key(self):
        if os.path.exists(self._DB_PASSWORD_FILENAME):
            self._load_existing_key()
        else:
            self._init_key()

    def _pad(self, message):
        return message + (self._BLOCK_SIZE - (len(message) % self._BLOCK_SIZE)) * chr(
            self._BLOCK_SIZE - (len(message) % self._BLOCK_SIZE))

    def _unpad(self, message: str):
        return message[0:-ord(message[len(message) - 1])]

    def enc(self, message: str):
        cipher_iv = Random.new().read(AES.block_size)
        cipher = AES.new(self._cipher_key, AES.MODE_CBC, cipher_iv)
        return base64.b64encode(cipher_iv + cipher.encrypt(self._pad(message).encode())).decode()

    def dec(self, enc_message):
        enc_message = base64.b64decode(enc_message)
        cipher_iv = enc_message[0:AES.block_size]
        cipher = AES.new(self._cipher_key, AES.MODE_CBC, cipher_iv)
        return self._unpad(cipher.decrypt(enc_message[AES.block_size:]).decode())


encryptor = Encryptor()
