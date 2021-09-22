import pytest
from tests.unit_tests.monkey_island.cc.services.utils.ciphertexts_for_encryption_test import (
    MALFORMED_CIPHER_TEXT_CORRUPTED,
    VALID_CIPHER_TEXT,
)

from monkey_island.cc.services.utils.password_encryption import (
    InvalidCredentialsError,
    PasswordBasedEncryptor,
)

MONKEY_CONFIGS_DIR_PATH = "monkey_configs"
STANDARD_PLAINTEXT_MONKEY_CONFIG_FILENAME = "monkey_config_standard.json"
PASSWORD = "hello123"
INCORRECT_PASSWORD = "goodbye321"


@pytest.mark.slow
def test_encrypt_decrypt_string(monkey_config_json):
    pb_encryptor = PasswordBasedEncryptor(PASSWORD)
    encrypted_config = pb_encryptor.encrypt(monkey_config_json)
    assert pb_encryptor.decrypt(encrypted_config) == monkey_config_json


@pytest.mark.slow
def test_decrypt_string__wrong_password(monkey_config_json):
    pb_encryptor = PasswordBasedEncryptor(INCORRECT_PASSWORD)
    with pytest.raises(InvalidCredentialsError):
        pb_encryptor.decrypt(VALID_CIPHER_TEXT)


@pytest.mark.slow
def test_decrypt_string__malformed_corrupted():
    pb_encryptor = PasswordBasedEncryptor(PASSWORD)
    with pytest.raises(ValueError):
        pb_encryptor.decrypt(MALFORMED_CIPHER_TEXT_CORRUPTED)


@pytest.mark.slow
def test_decrypt_string__no_password(monkey_config_json):
    pb_encryptor = PasswordBasedEncryptor("")
    with pytest.raises(InvalidCredentialsError):
        pb_encryptor.decrypt(VALID_CIPHER_TEXT)
