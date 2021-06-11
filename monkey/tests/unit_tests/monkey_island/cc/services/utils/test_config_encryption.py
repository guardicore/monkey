import pytest
from tests.unit_tests.monkey_island.cc.services.utils.cyphertexts_for_encryption_test import (
    MALFORMED_CYPHER_TEXT_CORRUPTED,
)

from monkey_island.cc.services.utils.config_encryption import (
    InvalidCredentialsError,
    decrypt_config,
    encrypt_config,
)

MONKEY_CONFIGS_DIR_PATH = "monkey_configs"
STANDARD_PLAINTEXT_MONKEY_CONFIG_FILENAME = "monkey_config_standard.json"
PASSWORD = "hello123"
INCORRECT_PASSWORD = "goodbye321"


def test_encrypt_decrypt_config(monkey_config):
    encrypted_config = encrypt_config(monkey_config, PASSWORD)
    assert decrypt_config(encrypted_config, PASSWORD) == monkey_config


def test_encrypt_decrypt_config__wrong_password(monkey_config):
    encrypted_config = encrypt_config(monkey_config, PASSWORD)
    with pytest.raises(InvalidCredentialsError):
        decrypt_config(encrypted_config, INCORRECT_PASSWORD)


def test_encrypt_decrypt_config__malformed_corrupted():
    with pytest.raises(ValueError):
        decrypt_config(MALFORMED_CYPHER_TEXT_CORRUPTED, PASSWORD)


def test_encrypt_decrypt_config__decrypt_no_password(monkey_config):
    encrypted_config = encrypt_config(monkey_config, PASSWORD)
    with pytest.raises(InvalidCredentialsError):
        decrypt_config(encrypted_config, "")
