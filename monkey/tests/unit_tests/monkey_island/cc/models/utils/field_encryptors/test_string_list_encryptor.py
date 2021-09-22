import pytest

from monkey_island.cc.models.utils.field_encryptors.string_list_encryptor import StringListEncryptor
from monkey_island.cc.server_utils.encryptor import initialize_encryptor

MOCK_STRING_LIST = ["test_1", "test_2"]
EMPTY_LIST = []


@pytest.fixture
def uses_encryptor(data_for_tests_dir):
    initialize_encryptor(data_for_tests_dir)


def test_string_list_encryptor(uses_encryptor):
    encrypted_list = StringListEncryptor.encrypt(MOCK_STRING_LIST)
    assert not encrypted_list == MOCK_STRING_LIST
    decrypted_list = StringListEncryptor.decrypt(encrypted_list)
    assert decrypted_list == MOCK_STRING_LIST


def test_string_list_encryptor__empty_list(uses_encryptor):
    encrypted_list = StringListEncryptor.encrypt(EMPTY_LIST)
    StringListEncryptor.decrypt(encrypted_list)
