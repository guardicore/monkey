import pytest
from tests.utils import get_file_sha256_hash

from monkey_island.cc.server_utils.encryption import (
    data_store_encryptor,
    get_datastore_encryptor,
    reset_datastore_encryptor,
    unlock_datastore_encryptor,
)

# Mark all tests in this module as slow
pytestmark = pytest.mark.slow

PLAINTEXT = b"Hello, Monkey!"
MOCK_SECRET = "53CR31"


@pytest.fixture(autouse=True)
def cleanup_encryptor():
    yield
    data_store_encryptor._encryptor = None


@pytest.fixture
def key_file(tmp_path):
    return tmp_path / "test_key.bin"


def test_encryption(tmp_path):
    unlock_datastore_encryptor(tmp_path, MOCK_SECRET)

    encrypted_data = get_datastore_encryptor().encrypt(PLAINTEXT)
    assert encrypted_data != PLAINTEXT

    decrypted_data = get_datastore_encryptor().decrypt(encrypted_data)
    assert decrypted_data == PLAINTEXT


def test_key_creation(key_file):
    assert not key_file.is_file()
    unlock_datastore_encryptor(key_file.parent, MOCK_SECRET, key_file.name)
    assert key_file.is_file()


def test_existing_key_reused(key_file):
    assert not key_file.is_file()

    unlock_datastore_encryptor(key_file.parent, MOCK_SECRET, key_file.name)
    key_file_hash_1 = get_file_sha256_hash(key_file)

    unlock_datastore_encryptor(key_file.parent, MOCK_SECRET, key_file.name)
    key_file_hash_2 = get_file_sha256_hash(key_file)

    assert key_file_hash_1 == key_file_hash_2


def test_reset_datastore_encryptor(key_file):
    unlock_datastore_encryptor(key_file.parent, MOCK_SECRET, key_file.name)
    key_file_hash_1 = get_file_sha256_hash(key_file)

    reset_datastore_encryptor(key_file.parent, MOCK_SECRET, key_file.name)
    key_file_hash_2 = get_file_sha256_hash(key_file)

    assert key_file_hash_1 != key_file_hash_2


def test_reset_when_encryptor_is_none(key_file):
    with key_file.open(mode="w") as f:
        f.write("")

    reset_datastore_encryptor(key_file.parent, MOCK_SECRET, key_file.name)
    assert (
        get_file_sha256_hash(key_file)
        != "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )


def test_reset_when_file_not_found(key_file):
    assert not key_file.is_file()
    reset_datastore_encryptor(key_file.parent, MOCK_SECRET, key_file.name)

    encrypted_data = get_datastore_encryptor().encrypt(PLAINTEXT)
    assert encrypted_data != PLAINTEXT

    decrypted_data = get_datastore_encryptor().decrypt(encrypted_data)
    assert decrypted_data == PLAINTEXT
