import pytest
from tests.unit_tests.monkey_island.cc.conftest import MOCK_PASSWORD, MOCK_USERNAME

from monkey_island.cc.server_utils.encryption import (
    DataStoreEncryptor,
    EncryptorNotInitializedError,
    data_store_encryptor,
    get_datastore_encryptor,
    initialize_datastore_encryptor,
    remove_old_datastore_key,
    setup_datastore_key,
)

PLAINTEXT = "Hello, Monkey!"


@pytest.mark.usefixtures("uses_encryptor")
def test_encryption(data_for_tests_dir):
    encrypted_data = get_datastore_encryptor().enc(PLAINTEXT)
    assert encrypted_data != PLAINTEXT

    decrypted_data = get_datastore_encryptor().dec(encrypted_data)
    assert decrypted_data == PLAINTEXT


@pytest.fixture
def initialized_key_dir(tmpdir):
    initialize_datastore_encryptor(tmpdir)
    setup_datastore_key(MOCK_USERNAME, MOCK_PASSWORD)
    yield tmpdir
    data_store_encryptor._encryptor = None


def test_key_creation(initialized_key_dir):
    assert (initialized_key_dir / DataStoreEncryptor._KEY_FILENAME).isfile()


def test_key_removal_fails_if_key_initialized(initialized_key_dir):
    remove_old_datastore_key()
    assert (initialized_key_dir / DataStoreEncryptor._KEY_FILENAME).isfile()


def test_key_removal(initialized_key_dir, monkeypatch):
    monkeypatch.setattr(DataStoreEncryptor, "is_key_setup", lambda _: False)
    remove_old_datastore_key()
    assert not (initialized_key_dir / DataStoreEncryptor._KEY_FILENAME).isfile()


def test_key_removal__no_key(tmpdir):
    initialize_datastore_encryptor(tmpdir)
    assert not (tmpdir / DataStoreEncryptor._KEY_FILENAME).isfile()
    # Make sure no error thrown when we try to remove an non-existing key
    remove_old_datastore_key()

    data_store_encryptor._encryptor = None


def test_encryptor_not_initialized():
    with pytest.raises(EncryptorNotInitializedError):
        remove_old_datastore_key()
        setup_datastore_key()


def test_setup_datastore_key(tmpdir):
    initialize_datastore_encryptor(tmpdir)
    assert not (tmpdir / DataStoreEncryptor._KEY_FILENAME).isfile()
    setup_datastore_key(MOCK_USERNAME, MOCK_PASSWORD)
    assert (tmpdir / DataStoreEncryptor._KEY_FILENAME).isfile()
    assert get_datastore_encryptor().is_key_setup()
