import pytest

from monkey_island.cc.server_utils.encryption import KeyBasedEncryptor
from monkey_island.cc.server_utils.encryption.encryption_key_types import EncryptionKey32Bytes

PLAINTEXT = "password"
# cryptography.fernet.Fernet.generate_key() generates a 32-bit key
PLAINTEXT_MULTIPLE_BLOCK_SIZE = "banana" * 32
PLAINTEXT_UTF8_1 = "slaptažodis"  # "password" in Lithuanian
PLAINTEXT_UTF8_2 = "弟"  # Japanese
PLAINTEXT_UTF8_3 = "ж"  # Ukranian

KEY = EncryptionKey32Bytes(
    b"!\x8a\xa9\x91\xf5\x124\xfcB\xdd\xb6\xee-\x8c\x82D\xe1p\x954\r\xf4\x1d5\xa9;\xef2|\x81\xb5\x15"
)

kb_encryptor = KeyBasedEncryptor(KEY)


def test_encrypt_decrypt_string_with_key():
    encrypted = kb_encryptor.encrypt(PLAINTEXT.encode())
    decrypted = kb_encryptor.decrypt(encrypted).decode()
    assert decrypted == PLAINTEXT


@pytest.mark.parametrize("plaintext", [PLAINTEXT_UTF8_1, PLAINTEXT_UTF8_2, PLAINTEXT_UTF8_3])
def test_encrypt_decrypt_string_utf8_with_key(plaintext):
    encrypted = kb_encryptor.encrypt(plaintext.encode())
    decrypted = kb_encryptor.decrypt(encrypted).decode()
    assert decrypted == plaintext


def test_encrypt_decrypt_string_multiple_block_size_with_key():
    encrypted = kb_encryptor.encrypt(PLAINTEXT_MULTIPLE_BLOCK_SIZE.encode())
    decrypted = kb_encryptor.decrypt(encrypted).decode()
    assert decrypted == PLAINTEXT_MULTIPLE_BLOCK_SIZE
