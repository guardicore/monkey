import pytest

from monkey_island.cc.server_utils.encryption import initialize_datastore_encryptor
from monkey_island.cc.server_utils.encryption.dict_encryption.field_encryptors import (
    StringListEncryptor,
)

MOCK_STRING_LIST = ["test_1", "test_2"]
EMPTY_LIST = []


@pytest.fixture
def uses_encryptor(data_for_tests_dir):
    initialize_datastore_encryptor(data_for_tests_dir)


def test_encryption_and_decryption(uses_encryptor):
    encrypted_list = StringListEncryptor.encrypt(MOCK_STRING_LIST)
    assert not encrypted_list == MOCK_STRING_LIST
    decrypted_list = StringListEncryptor.decrypt(encrypted_list)
    assert decrypted_list == MOCK_STRING_LIST


def test_empty_list(uses_encryptor):
    # Tests that no errors are raised
    encrypted_list = StringListEncryptor.encrypt(EMPTY_LIST)
    StringListEncryptor.decrypt(encrypted_list)
