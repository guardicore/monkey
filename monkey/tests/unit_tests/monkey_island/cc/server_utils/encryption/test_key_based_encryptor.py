import pytest

from monkey_island.cc.server_utils.encryption import KeyBasedEncryptor

PLAINTEXT = "password"
PLAINTEXT_MULTIPLE_BLOCK_SIZE = "banana" * KeyBasedEncryptor._BLOCK_SIZE
PLAINTEXT_UTF8_1 = "slaptažodis"  # "password" in Lithuanian
PLAINTEXT_UTF8_2 = "弟"  # Japanese
PLAINTEXT_UTF8_3 = "ж"  # Ukranian

KEY = b"\x84\xd4qA\xb5\xd4Y\x9bH.\x14\xab\xd8\xc7+g\x12\xfa\x80'%\xfd#\xf8c\x94\xb9\x96_\xf4\xc51"

kb_encryptor = KeyBasedEncryptor(KEY)


def test_encrypt_decrypt_string_with_key():
    encrypted = kb_encryptor.encrypt(PLAINTEXT)
    decrypted = kb_encryptor.decrypt(encrypted)
    assert decrypted == PLAINTEXT


@pytest.mark.parametrize("plaintext", [PLAINTEXT_UTF8_1, PLAINTEXT_UTF8_2, PLAINTEXT_UTF8_3])
def test_encrypt_decrypt_string_utf8_with_key(plaintext):
    encrypted = kb_encryptor.encrypt(plaintext)
    decrypted = kb_encryptor.decrypt(encrypted)
    assert decrypted == plaintext


def test_encrypt_decrypt_string_multiple_block_size_with_key():
    encrypted = kb_encryptor.encrypt(PLAINTEXT_MULTIPLE_BLOCK_SIZE)
    decrypted = kb_encryptor.decrypt(encrypted)
    assert decrypted == PLAINTEXT_MULTIPLE_BLOCK_SIZE
