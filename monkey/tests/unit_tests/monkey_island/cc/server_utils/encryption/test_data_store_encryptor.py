import pytest

from monkey_island.cc.server_utils.encryption import (
    data_store_encryptor,
    get_datastore_encryptor,
    initialize_datastore_encryptor,
    remove_old_datastore_key,
)

PLAINTEXT = "Hello, Monkey!"
MOCK_SECRET = "53CR31"


@pytest.mark.usefixtures("uses_encryptor")
def test_encryption(data_for_tests_dir):
    encrypted_data = get_datastore_encryptor().encrypt(PLAINTEXT)
    assert encrypted_data != PLAINTEXT

    decrypted_data = get_datastore_encryptor().decrypt(encrypted_data)
    assert decrypted_data == PLAINTEXT


@pytest.fixture
def cleanup_encryptor():
    yield
    data_store_encryptor._encryptor = None


@pytest.mark.usefixtures("cleanup_encryptor")
@pytest.fixture
def initialized_encryptor_dir(tmpdir):
    initialize_datastore_encryptor(tmpdir, MOCK_SECRET)
    return tmpdir


def test_key_creation(initialized_encryptor_dir):
    assert (initialized_encryptor_dir / data_store_encryptor._KEY_FILENAME).isfile()


def test_key_removal(initialized_encryptor_dir):
    remove_old_datastore_key(initialized_encryptor_dir)
    assert not (initialized_encryptor_dir / data_store_encryptor._KEY_FILENAME).isfile()


def test_key_removal__no_key(tmpdir):
    assert not (tmpdir / data_store_encryptor._KEY_FILENAME).isfile()
    # Make sure no error thrown when we try to remove an non-existing key
    remove_old_datastore_key(tmpdir)
    data_store_encryptor._factory = None


@pytest.mark.usefixtures("cleanup_encryptor")
def test_key_file_encryption(tmpdir, monkeypatch):
    monkeypatch.setattr(data_store_encryptor, "_get_random_bytes", lambda: PLAINTEXT.encode())
    initialize_datastore_encryptor(tmpdir, MOCK_SECRET)
    key_file_path = data_store_encryptor._get_key_file_path(tmpdir)
    key_file_contents = open(key_file_path, "rb").read()
    assert not key_file_contents == PLAINTEXT.encode()

    key_based_encryptor = data_store_encryptor._load_existing_key(key_file_path, MOCK_SECRET)
    assert key_based_encryptor._key == PLAINTEXT.encode()
