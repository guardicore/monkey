import pytest
from tests.unit_tests.monkey_island.cc.services.utils.ciphertexts_for_encryption_test import (
    MALFORMED_CIPHER_TEXT_CORRUPTED,
    VALID_CIPHER_TEXT,
)

from monkey_island.cc.server_utils.encryption import (
    InvalidCiphertextError,
    InvalidCredentialsError,
    PasswordBasedStringEncryptor,
)

# Mark all tests in this module as slow
pytestmark = pytest.mark.slow

MONKEY_CONFIGS_DIR_PATH = "monkey_configs"
STANDARD_PLAINTEXT_MONKEY_CONFIG_FILENAME = "monkey_config_standard.json"
FLAT_PLAINTEXT_MONKEY_CONFIG_FILENAME = "flat_config.json"
PASSWORD = "hello123"
INCORRECT_PASSWORD = "goodbye321"


def test_encrypt_decrypt_string(monkey_config_json):
    pb_encryptor = PasswordBasedStringEncryptor(PASSWORD)
    encrypted_config = pb_encryptor.encrypt(monkey_config_json)
    assert pb_encryptor.decrypt(encrypted_config) == monkey_config_json


def test_decrypt_string__wrong_password(monkey_config_json):
    pb_encryptor = PasswordBasedStringEncryptor(INCORRECT_PASSWORD)
    with pytest.raises(InvalidCredentialsError):
        pb_encryptor.decrypt(VALID_CIPHER_TEXT)


def test_decrypt_string__malformed_corrupted():
    pb_encryptor = PasswordBasedStringEncryptor(PASSWORD)
    with pytest.raises(ValueError):
        pb_encryptor.decrypt(MALFORMED_CIPHER_TEXT_CORRUPTED)


def test_decrypt_string__no_password(monkey_config_json):
    pb_encryptor = PasswordBasedStringEncryptor("")
    with pytest.raises(InvalidCredentialsError):
        pb_encryptor.decrypt(VALID_CIPHER_TEXT)


def test_decrypt_string__invalid_cyphertext(monkey_config_json):
    pb_encryptor = PasswordBasedStringEncryptor("")
    with pytest.raises(InvalidCiphertextError):
        pb_encryptor.decrypt("")
