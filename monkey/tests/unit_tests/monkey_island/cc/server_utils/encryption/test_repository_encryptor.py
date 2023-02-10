import random
import string

import pytest
from tests.utils import get_file_sha256_hash

from monkey_island.cc.server_utils.encryption import (
    LockedKeyError,
    RepositoryEncryptor,
    ResetKeyError,
    UnlockError,
)

# Mark all tests in this module as slow
pytestmark = pytest.mark.slow

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


def test_existing_key_reused__lock(encryptor, key_file):
    assert not key_file.is_file()

    encryptor.unlock(SECRET)
    key_file_hash_1 = get_file_sha256_hash(key_file)

    encryptor.lock()

    encryptor.unlock(SECRET)
    key_file_hash_2 = get_file_sha256_hash(key_file)

    assert key_file_hash_1 == key_file_hash_2


def test_unlock_os_error(encryptor, key_file):
    key_file.mkdir()

    with pytest.raises(UnlockError):
        encryptor.unlock(SECRET)


def test_unlock_wrong_password(encryptor):
    encryptor.unlock(SECRET)

    with pytest.raises(UnlockError):
        encryptor.unlock(b"WRONG_PASSWORD")


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


def test_reset(encryptor, key_file):
    encryptor.unlock(SECRET)
    key_file_hash_1 = get_file_sha256_hash(key_file)

    encryptor.reset_key()
    encryptor.unlock(SECRET)
    key_file_hash_2 = get_file_sha256_hash(key_file)

    assert key_file_hash_1 != key_file_hash_2


def test_encrypt_after_reset(encryptor, key_file):
    encryptor.unlock(SECRET)
    encryptor.reset_key()

    with pytest.raises(LockedKeyError):
        encryptor.encrypt(PLAINTEXT)


def test_reset_before_unlock(encryptor):
    # Test will fail if an exception is raised
    encryptor.reset_key()


def test_reset_key_error(key_file):
    class UnlinkErrorWrapper(key_file.__class__):
        def unlink(self):
            raise OSError("Can't delete file")

    encryptor = RepositoryEncryptor(UnlinkErrorWrapper(key_file))
    encryptor.unlock(SECRET)
    encryptor.lock()

    with pytest.raises(ResetKeyError):
        encryptor.reset_key()
