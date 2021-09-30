import os

import pytest
from tests.unit_tests.monkey_island.cc.conftest import ENCRYPTOR_SECRET

from monkey_island.cc.server_utils.encryption import (
    DataStoreEncryptor,
    get_datastore_encryptor,
    initialize_datastore_encryptor,
)
from monkey_island.cc.server_utils.encryption.data_store_encryptor import setup_datastore_key

PLAINTEXT = "Hello, Monkey!"


@pytest.mark.usefixtures("uses_encryptor")
def test_encryption(data_for_tests_dir):
    encrypted_data = get_datastore_encryptor().enc(PLAINTEXT)
    assert encrypted_data != PLAINTEXT

    decrypted_data = get_datastore_encryptor().dec(encrypted_data)
    assert decrypted_data == PLAINTEXT


def test_create_new_password_file(tmpdir):
    initialize_datastore_encryptor(tmpdir)
    setup_datastore_key(ENCRYPTOR_SECRET)
    assert os.path.isfile(os.path.join(tmpdir, DataStoreEncryptor._KEY_FILENAME))
