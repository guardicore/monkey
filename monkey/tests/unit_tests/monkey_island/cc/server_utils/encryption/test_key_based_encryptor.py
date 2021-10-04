from monkey_island.cc.server_utils.encryption import KeyBasedEncryptor

PLAINTEXT = "password"
PLAINTEXT_UTF8 = "slaptažodis"  # "password" in Lithuanian
KEY = b"\x84\xd4qA\xb5\xd4Y\x9bH.\x14\xab\xd8\xc7+g\x12\xfa\x80'%\xfd#\xf8c\x94\xb9\x96_\xf4\xc51"

kb_encryptor = KeyBasedEncryptor(KEY)


def test_encrypt_decrypt_string_with_key():
    encrypted = kb_encryptor.encrypt(PLAINTEXT)
    decrypted = kb_encryptor.decrypt(encrypted)
    assert decrypted == PLAINTEXT


def test_encrypt_decrypt_string_utf8_with_key():
    encrypted = kb_encryptor.encrypt(PLAINTEXT_UTF8)
    decrypted = kb_encryptor.decrypt(encrypted)
    assert decrypted == PLAINTEXT_UTF8
