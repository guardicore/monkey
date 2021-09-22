import pytest
from tests.unit_tests.monkey_island.cc.services.utils.ciphertexts_for_encryption_test import (
    MALFORMED_CIPHER_TEXT_CORRUPTED,
)
from tests.unit_tests.monkey_island.cc.services.utils.test_encryption import PASSWORD

from common.utils.exceptions import InvalidConfigurationError
from monkey_island.cc.resources.configuration_import import ConfigurationImport
from monkey_island.cc.services.utils.encryption import encrypt_string


def test_is_config_encrypted__json(monkey_config_json):
    assert not ConfigurationImport.is_config_encrypted(monkey_config_json)


@pytest.mark.slow
def test_is_config_encrypted__ciphertext(monkey_config_json):
    encrypted_config = encrypt_string(monkey_config_json, PASSWORD)
    assert ConfigurationImport.is_config_encrypted(encrypted_config)


def test_is_config_encrypted__corrupt_ciphertext():
    with pytest.raises(InvalidConfigurationError):
        assert ConfigurationImport.is_config_encrypted(MALFORMED_CIPHER_TEXT_CORRUPTED)


def test_is_config_encrypted__unknown_format():
    with pytest.raises(InvalidConfigurationError):
        assert ConfigurationImport.is_config_encrypted("ABC")
