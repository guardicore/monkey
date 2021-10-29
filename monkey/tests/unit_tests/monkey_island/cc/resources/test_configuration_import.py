import pytest
from tests.unit_tests.monkey_island.cc.server_utils.encryption.test_password_based_encryption import (  # noqa: E501
    PASSWORD,
)
from tests.unit_tests.monkey_island.cc.services.utils.ciphertexts_for_encryption_test import (
    MALFORMED_CIPHER_TEXT_CORRUPTED,
)

from common.utils.exceptions import InvalidConfigurationError
from monkey_island.cc.resources.configuration_import import ConfigurationImport
from monkey_island.cc.server_utils.encryption import PasswordBasedStringEncryptor


def test_is_config_encrypted__json(monkey_config_json):
    assert not ConfigurationImport.is_config_encrypted(monkey_config_json)


@pytest.mark.slow
def test_is_config_encrypted__ciphertext(monkey_config_json):
    pb_encryptor = PasswordBasedStringEncryptor(PASSWORD)
    encrypted_config = pb_encryptor.encrypt(monkey_config_json)
    assert ConfigurationImport.is_config_encrypted(encrypted_config)


def test_is_config_encrypted__corrupt_ciphertext():
    with pytest.raises(InvalidConfigurationError):
        assert ConfigurationImport.is_config_encrypted(MALFORMED_CIPHER_TEXT_CORRUPTED)


def test_is_config_encrypted__unknown_format():
    with pytest.raises(InvalidConfigurationError):
        assert ConfigurationImport.is_config_encrypted("ABC")
