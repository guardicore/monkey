import pytest

from common.utils.file_utils import get_file_sha256_hash
from monkey_island.cc.server_utils.encryption import (
    data_store_encryptor,
    get_datastore_encryptor,
    initialize_datastore_encryptor,
    reinitialize_datastore_encryptor,
)

# Mark all tests in this module as slow
pytestmark = pytest.mark.slow

PLAINTEXT = "Hello, Monkey!"
MOCK_SECRET = "53CR31"

KEY_FILENAME = "test_key.bin"


@pytest.fixture(autouse=True)
def cleanup_encryptor():
    yield
    data_store_encryptor._encryptor = None


@pytest.fixture
def key_file(tmp_path):
    return tmp_path / KEY_FILENAME


def test_encryption(tmp_path):
    initialize_datastore_encryptor(tmp_path, MOCK_SECRET, KEY_FILENAME)

    encrypted_data = get_datastore_encryptor().encrypt(PLAINTEXT)
    assert encrypted_data != PLAINTEXT

    decrypted_data = get_datastore_encryptor().decrypt(encrypted_data)
    assert decrypted_data == PLAINTEXT


def test_key_creation(key_file, tmp_path):
    assert not key_file.is_file()
    initialize_datastore_encryptor(tmp_path, MOCK_SECRET, KEY_FILENAME)
    assert key_file.is_file()


def test_existing_key_reused(key_file, tmp_path):
    assert not key_file.is_file()

    initialize_datastore_encryptor(tmp_path, MOCK_SECRET, KEY_FILENAME)
    key_file_hash_1 = get_file_sha256_hash(key_file)

    initialize_datastore_encryptor(tmp_path, MOCK_SECRET, KEY_FILENAME)
    key_file_hash_2 = get_file_sha256_hash(key_file)

    assert key_file_hash_1 == key_file_hash_2


def test_key_removal(key_file, tmp_path):
    initialize_datastore_encryptor(tmp_path, MOCK_SECRET, KEY_FILENAME)
    assert key_file.is_file()

    get_datastore_encryptor().erase_key()
    assert not key_file.is_file()


def test_key_removal__no_key(key_file, tmp_path):
    assert not key_file.is_file()
    initialize_datastore_encryptor(tmp_path, MOCK_SECRET, KEY_FILENAME)
    assert key_file.is_file()

    get_datastore_encryptor().erase_key()
    assert not key_file.is_file()

    # Make sure no error thrown when we try to remove an non-existing key
    get_datastore_encryptor().erase_key()


def test_reinitialize_datastore_encryptor(key_file, tmp_path):
    initialize_datastore_encryptor(tmp_path, MOCK_SECRET, KEY_FILENAME)
    key_file_hash_1 = get_file_sha256_hash(key_file)

    reinitialize_datastore_encryptor(tmp_path, MOCK_SECRET, KEY_FILENAME)
    key_file_hash_2 = get_file_sha256_hash(key_file)

    assert key_file_hash_1 != key_file_hash_2
