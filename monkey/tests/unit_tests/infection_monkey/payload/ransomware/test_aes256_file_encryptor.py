import filecmp
from pathlib import Path
from shutil import copy

import pyAesCrypt
import pytest

from common.types import FileExtension
from infection_monkey.payload.ransomware.aes_256_file_encryptor import AES256FileEncryptor

FILE_NAME = "propagation_credentials.py"
PASSWORD = "m0nk3y"


@pytest.fixture
def original_file(data_for_tests_dir: Path) -> Path:
    return data_for_tests_dir / FILE_NAME


@pytest.fixture
def src_file(original_file: Path, tmp_path: Path) -> Path:
    copy(original_file, tmp_path)

    return tmp_path / FILE_NAME


@pytest.mark.parametrize("extension", [FileExtension(".m0nk3y"), FileExtension(".crypto")])
def test_encrypt_decrypt_with_extension(
    original_file: Path, src_file: Path, extension: FileExtension
):
    expected_dst_file = Path(str(src_file) + extension)

    encryptor = AES256FileEncryptor(PASSWORD, extension)
    encryptor(src_file)

    assert not src_file.exists()
    assert expected_dst_file.exists()
    assert not filecmp.cmp(original_file, expected_dst_file)

    decrypted_file = expected_dst_file.with_suffix(".decrypted")
    pyAesCrypt.decryptFile(expected_dst_file, decrypted_file, PASSWORD)

    assert filecmp.cmp(original_file, decrypted_file)


def test_encrypt_decrypt_no_extension(original_file: Path, src_file: Path):
    encryptor = AES256FileEncryptor(PASSWORD)
    encryptor(src_file)

    assert src_file.exists()
    assert not filecmp.cmp(original_file, src_file)

    decrypted_file = src_file.with_suffix(".decrypted")
    pyAesCrypt.decryptFile(src_file, decrypted_file, PASSWORD)

    assert filecmp.cmp(original_file, decrypted_file)
