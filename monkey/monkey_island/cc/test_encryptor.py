import os

from monkey_island.cc.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.encryptor import initialize_encryptor, encryptor


TEST_DATA_DIR = os.path.join(MONKEY_ISLAND_ABS_PATH, "cc", "testing")
PASSWORD_FILENAME = "mongo_key.bin"

PLAINTEXT = "Hello, Monkey!"
CYPHERTEXT = "vKgvD6SjRyIh1dh2AM/rnTa0NI/vjfwnbZLbMocWtE4e42WJmSUz2ordtbQrH1Fq"


def test_aes_cbc_encryption():
    initialize_encryptor(TEST_DATA_DIR)

    assert encryptor().enc(PLAINTEXT) != PLAINTEXT


def test_aes_cbc_decryption():
    initialize_encryptor(TEST_DATA_DIR)

    assert encryptor().dec(CYPHERTEXT) == PLAINTEXT


def test_create_new_password_file(tmpdir):
    initialize_encryptor(tmpdir)

    assert os.path.isfile(os.path.join(tmpdir, PASSWORD_FILENAME))
