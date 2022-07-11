import random
import string

import pytest

from common.utils.file_utils import get_file_sha256_hash
from monkey_island.cc.server_utils.encryption import LockedKeyError, RepositoryEncryptor

PLAINTEXT = b"Hello, Monkey!"
SECRET = b"53CR31"


@pytest.fixture
def key_file(tmp_path):
    return tmp_path / "test_key.bin"


@pytest.fixture
def encryptor(key_file):
    return RepositoryEncryptor(key_file)


def test_encryption(encryptor):
    plaintext = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(128)  # noqa: DUO102
    ).encode()
    encryptor.unlock(SECRET)

    encrypted_data = encryptor.encrypt(plaintext)
    assert encrypted_data != plaintext

    decrypted_data = encryptor.decrypt(encrypted_data)
    assert decrypted_data == plaintext


def test_key_creation(encryptor, key_file):
    assert not key_file.is_file()
    encryptor.unlock(SECRET)
    assert key_file.is_file()


def test_existing_key_reused(encryptor, key_file):
    assert not key_file.is_file()

    encryptor.unlock(SECRET)
    key_file_hash_1 = get_file_sha256_hash(key_file)

    encryptor.unlock(SECRET)
    key_file_hash_2 = get_file_sha256_hash(key_file)

    assert key_file_hash_1 == key_file_hash_2


def test_use_locked_encryptor__encrypt(encryptor):
    with pytest.raises(LockedKeyError):
        encryptor.encrypt(PLAINTEXT)


def test_use_locked_encryptor__decrypt(encryptor):
    with pytest.raises(LockedKeyError):
        encryptor.decrypt(PLAINTEXT)


def test_lock(encryptor):
    encryptor.unlock(SECRET)
    encrypted_data = encryptor.encrypt(PLAINTEXT)
    encryptor.lock()

    with pytest.raises(LockedKeyError):
        encryptor.decrypt(encrypted_data)
