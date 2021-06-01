import json
import os

import pytest

from monkey_island.cc.services.utils.config_encryption import decrypt_config, encrypt_config

MONKEY_CONFIGS_DIR_PATH = "monkey_configs"
STANDARD_PLAINTEXT_MONKEY_CONFIG_FILENAME = "monkey_config_standard.json"

PASSWORD = "hello123"


@pytest.fixture
def plaintext_config(data_for_tests_dir):
    plaintext_monkey_config_standard_path = os.path.join(
        data_for_tests_dir, MONKEY_CONFIGS_DIR_PATH, STANDARD_PLAINTEXT_MONKEY_CONFIG_FILENAME
    )
    plaintext_config = json.loads(open(plaintext_monkey_config_standard_path, "r").read())
    return plaintext_config


def test_encrypt_decrypt_config(plaintext_config):
    encrypted_config = encrypt_config(plaintext_config, PASSWORD)
    encrypted_config = encrypted_config
    assert decrypt_config(encrypted_config, PASSWORD) == plaintext_config
