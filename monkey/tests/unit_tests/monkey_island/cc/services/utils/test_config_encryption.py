import json
import os

import pytest
from tests.unit_tests.monkey_island.cc.services.utils.cyphertexts_for_encryption_test import (
    MALFORMED_CYPHER_TEXT_CORRUPTED,
    MALFORMED_CYPHER_TEXT_TOO_SHORT,
)

from common.utils.exceptions import InvalidCredentialsError, NoCredentialsError
from monkey_island.cc.services.utils.config_encryption import decrypt_config, encrypt_config

MONKEY_CONFIGS_DIR_PATH = "monkey_configs"
STANDARD_PLAINTEXT_MONKEY_CONFIG_FILENAME = "monkey_config_standard.json"
PASSWORD = "hello123"
INCORRECT_PASSWORD = "goodbye321"


@pytest.fixture
def plaintext_config(data_for_tests_dir):
    plaintext_monkey_config_standard_path = os.path.join(
        data_for_tests_dir, MONKEY_CONFIGS_DIR_PATH, STANDARD_PLAINTEXT_MONKEY_CONFIG_FILENAME
    )
    plaintext_config = json.loads(open(plaintext_monkey_config_standard_path, "r").read())
    return plaintext_config


def test_encrypt_decrypt_config(plaintext_config):
    encrypted_config = encrypt_config(plaintext_config, PASSWORD)
    assert decrypt_config(encrypted_config, PASSWORD) == plaintext_config


def test_encrypt_decrypt_config__wrong_password(plaintext_config):
    encrypted_config = encrypt_config(plaintext_config, PASSWORD)
    with pytest.raises(InvalidCredentialsError):
        decrypt_config(encrypted_config, INCORRECT_PASSWORD)


def test_encrypt_decrypt_config__malformed():
    with pytest.raises(ValueError):
        decrypt_config(MALFORMED_CYPHER_TEXT_TOO_SHORT, PASSWORD)
    with pytest.raises(ValueError):
        decrypt_config(MALFORMED_CYPHER_TEXT_CORRUPTED, PASSWORD)


def test_encrypt_decrypt_config__decrypt_no_password(plaintext_config):
    encrypted_config = encrypt_config(plaintext_config, PASSWORD)
    with pytest.raises(NoCredentialsError):
        decrypt_config(encrypted_config, "")
