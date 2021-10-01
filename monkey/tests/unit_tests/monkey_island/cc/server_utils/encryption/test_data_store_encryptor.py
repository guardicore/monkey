import pytest
from tests.unit_tests.monkey_island.cc.conftest import MOCK_PASSWORD, MOCK_USERNAME

from monkey_island.cc.server_utils.encryption import (
    FactoryNotInitializedError,
    data_store_encryptor,
    encryptor_factory,
    get_datastore_encryptor,
    initialize_datastore_encryptor,
    initialize_encryptor_factory,
    remove_old_datastore_key,
)
from monkey_island.cc.server_utils.encryption.data_store_encryptor import DataStoreEncryptor
from monkey_island.cc.server_utils.encryption.encryptor_factory import EncryptorFactory

PLAINTEXT = "Hello, Monkey!"


@pytest.mark.usefixtures("uses_encryptor")
def test_encryption(data_for_tests_dir):
    encrypted_data = get_datastore_encryptor().enc(PLAINTEXT)
    assert encrypted_data != PLAINTEXT

    decrypted_data = get_datastore_encryptor().dec(encrypted_data)
    assert decrypted_data == PLAINTEXT


@pytest.fixture
def initialized_key_dir(tmpdir):
    initialize_encryptor_factory(tmpdir)
    initialize_datastore_encryptor(MOCK_USERNAME, MOCK_PASSWORD)
    yield tmpdir
    data_store_encryptor._encryptor = None
    encryptor_factory._factory = None


def test_key_creation(initialized_key_dir):
    assert (initialized_key_dir / EncryptorFactory._KEY_FILENAME).isfile()


def test_key_removal(initialized_key_dir):
    remove_old_datastore_key()
    assert not (initialized_key_dir / EncryptorFactory._KEY_FILENAME).isfile()


def test_key_removal__no_key(tmpdir):
    initialize_encryptor_factory(tmpdir)
    assert not (tmpdir / EncryptorFactory._KEY_FILENAME).isfile()
    # Make sure no error thrown when we try to remove an non-existing key
    remove_old_datastore_key()
    encryptor_factory._factory = None


def test_encryptor_not_initialized():
    with pytest.raises(FactoryNotInitializedError):
        remove_old_datastore_key()
        initialize_datastore_encryptor(MOCK_USERNAME, MOCK_PASSWORD)


def test_initialize_encryptor(tmpdir):
    initialize_encryptor_factory(tmpdir)
    assert not (tmpdir / EncryptorFactory._KEY_FILENAME).isfile()
    initialize_datastore_encryptor(MOCK_USERNAME, MOCK_PASSWORD)
    assert (tmpdir / EncryptorFactory._KEY_FILENAME).isfile()


def test_key_file_encryption(tmpdir, monkeypatch):
    monkeypatch(DataStoreEncryptor._)
