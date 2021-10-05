import pytest

from monkey_island.cc.server_utils.encryption import (
    data_store_encryptor,
    get_datastore_encryptor,
    initialize_datastore_encryptor,
    remove_old_datastore_key,
)

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


@pytest.mark.slow
def test_encryption(tmp_path):
    initialize_datastore_encryptor(tmp_path, MOCK_SECRET, KEY_FILENAME)

    encrypted_data = get_datastore_encryptor().encrypt(PLAINTEXT)
    assert encrypted_data != PLAINTEXT

    decrypted_data = get_datastore_encryptor().decrypt(encrypted_data)
    assert decrypted_data == PLAINTEXT


@pytest.mark.slow
def test_key_creation(key_file, tmp_path):
    assert not key_file.is_file()
    initialize_datastore_encryptor(tmp_path, MOCK_SECRET, KEY_FILENAME)
    assert key_file.is_file()


@pytest.mark.slow
def test_key_removal(key_file, tmp_path):
    initialize_datastore_encryptor(tmp_path, MOCK_SECRET, KEY_FILENAME)
    assert key_file.is_file()

    remove_old_datastore_key()
    assert not key_file.is_file()


def test_key_removal__no_key(key_file):
    assert not key_file.is_file()
    # Make sure no error thrown when we try to remove an non-existing key
    remove_old_datastore_key()


def test_key_removal__no_key_2(key_file, tmp_path):
    assert not key_file.is_file()
    initialize_datastore_encryptor(tmp_path, MOCK_SECRET, KEY_FILENAME)
    assert key_file.is_file()

    key_file.unlink()
    assert not key_file.is_file()

    # Make sure no error thrown when we try to remove an non-existing key
    get_datastore_encryptor().erase_key()
