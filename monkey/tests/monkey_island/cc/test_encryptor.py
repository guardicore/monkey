import os

from monkey_island.cc.server_utils.encryptor import get_encryptor, initialize_encryptor

PASSWORD_FILENAME = "mongo_key.bin"

PLAINTEXT = "Hello, Monkey!"
CYPHERTEXT = "vKgvD6SjRyIh1dh2AM/rnTa0NI/vjfwnbZLbMocWtE4e42WJmSUz2ordtbQrH1Fq"


def test_aes_cbc_encryption(resources_dir):
    initialize_encryptor(resources_dir)

    assert get_encryptor().enc(PLAINTEXT) != PLAINTEXT


def test_aes_cbc_decryption(resources_dir):
    initialize_encryptor(resources_dir)

    assert get_encryptor().dec(CYPHERTEXT) == PLAINTEXT


def test_aes_cbc_enc_dec(resources_dir):
    initialize_encryptor(resources_dir)

    assert get_encryptor().dec(get_encryptor().enc(PLAINTEXT)) == PLAINTEXT


def test_create_new_password_file(tmpdir):
    initialize_encryptor(tmpdir)

    assert os.path.isfile(os.path.join(tmpdir, PASSWORD_FILENAME))
