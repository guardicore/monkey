import pytest

from monkey_island.cc.server_utils.encryption import KeyBasedEncryptor

PLAINTEXT = "password"
PLAINTEXT_MULTIPLE_BLOCK_SIZE = "banana" * KeyBasedEncryptor._BLOCK_SIZE
PLAINTEXT_UTF8_1 = "slaptažodis"  # "password" in Lithuanian
PLAINTEXT_UTF8_2 = "弟"  # Japanese
PLAINTEXT_UTF8_3 = "ж"  # Ukranian

KEY = b"FK-jSjEPwBPlg-LxxdEti8-_9EN036afsR8DHuXS0Zo="

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
