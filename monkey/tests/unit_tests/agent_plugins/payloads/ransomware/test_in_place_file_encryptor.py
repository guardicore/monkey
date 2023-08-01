import os
from pathlib import Path

import pytest
from agent_plugins.payloads.ransomware.src.bit_manipulators import flip_bits
from agent_plugins.payloads.ransomware.src.in_place_file_encryptor import InPlaceFileEncryptor
from agent_plugins.payloads.ransomware.src.typedef import FileEncryptorCallable
from tests.unit_tests.agent_plugins.payloads.ransomware.ransomware_target_files import (
    ALL_ZEROS_PDF,
    ALL_ZEROS_PDF_CLEARTEXT_SHA256,
    ALL_ZEROS_PDF_ENCRYPTED_SHA256,
    TEST_KEYBOARD_TXT,
    TEST_KEYBOARD_TXT_CLEARTEXT_SHA256,
    TEST_KEYBOARD_TXT_ENCRYPTED_SHA256,
)
from tests.utils import get_file_sha256_hash

from common.types import FileExtension

EXTENSION = FileExtension(".m0nk3y")


def with_extension(filename) -> str:
    return f"{filename}{EXTENSION}"


@pytest.fixture(scope="module")
def in_place_bitflip_file_encryptor() -> FileEncryptorCallable:
    return InPlaceFileEncryptor(encrypt_bytes=flip_bits, chunk_size=64)


@pytest.mark.parametrize(
    "file_name,cleartext_hash,encrypted_hash",
    [
        (TEST_KEYBOARD_TXT, TEST_KEYBOARD_TXT_CLEARTEXT_SHA256, TEST_KEYBOARD_TXT_ENCRYPTED_SHA256),
        (ALL_ZEROS_PDF, ALL_ZEROS_PDF_CLEARTEXT_SHA256, ALL_ZEROS_PDF_ENCRYPTED_SHA256),
    ],
)
def test_file_encrypted(
    in_place_bitflip_file_encryptor: FileEncryptorCallable,
    ransomware_target: Path,
    file_name: str,
    cleartext_hash: str,
    encrypted_hash: str,
):
    test_keyboard = ransomware_target / file_name

    assert get_file_sha256_hash(test_keyboard) == cleartext_hash

    in_place_bitflip_file_encryptor(test_keyboard)

    assert get_file_sha256_hash(test_keyboard) == encrypted_hash


def test_file_encrypted_in_place(
    in_place_bitflip_file_encryptor: FileEncryptorCallable, ransomware_target: Path
):
    test_keyboard = ransomware_target / TEST_KEYBOARD_TXT

    expected_inode = os.stat(test_keyboard).st_ino
    in_place_bitflip_file_encryptor(test_keyboard)
    actual_inode = os.stat(test_keyboard).st_ino

    assert expected_inode == actual_inode


def test_encrypted_file_has_new_extension(ransomware_target: Path):
    test_keyboard = ransomware_target / TEST_KEYBOARD_TXT
    encrypted_test_keyboard = ransomware_target / with_extension(TEST_KEYBOARD_TXT)
    encryptor = InPlaceFileEncryptor(encrypt_bytes=flip_bits, new_file_extension=EXTENSION)

    encryptor(test_keyboard)

    assert not test_keyboard.exists()
    assert encrypted_test_keyboard.exists()
    assert get_file_sha256_hash(encrypted_test_keyboard) == TEST_KEYBOARD_TXT_ENCRYPTED_SHA256
