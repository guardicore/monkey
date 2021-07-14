import os

import pytest
from tests.unit_tests.infection_monkey.ransomware.ransomware_target_files import (
    ALL_ZEROS_PDF,
    ALL_ZEROS_PDF_CLEARTEXT_SHA256,
    ALL_ZEROS_PDF_ENCRYPTED_SHA256,
    TEST_KEYBOARD_TXT,
    TEST_KEYBOARD_TXT_CLEARTEXT_SHA256,
    TEST_KEYBOARD_TXT_ENCRYPTED_SHA256,
)
from tests.utils import hash_file

from infection_monkey.ransomware.in_place_encryptor import InPlaceEncryptor
from infection_monkey.utils.bit_manipulators import flip_bits

EXTENSION = ".m0nk3y"


def with_extension(filename):
    return f"{filename}{EXTENSION}"


@pytest.fixture(scope="module")
def in_place_bitflip_encryptor():
    return InPlaceEncryptor(encrypt_bytes=flip_bits, chunk_size=64)


@pytest.mark.parametrize("invalid_extension", ["no_dot", ".has/slash", ".has\\slash"])
def test_invalid_file_extension(invalid_extension):
    with pytest.raises(ValueError):
        InPlaceEncryptor(encrypt_bytes=None, new_file_extension=invalid_extension)


@pytest.mark.parametrize(
    "file_name,cleartext_hash,encrypted_hash",
    [
        (TEST_KEYBOARD_TXT, TEST_KEYBOARD_TXT_CLEARTEXT_SHA256, TEST_KEYBOARD_TXT_ENCRYPTED_SHA256),
        (ALL_ZEROS_PDF, ALL_ZEROS_PDF_CLEARTEXT_SHA256, ALL_ZEROS_PDF_ENCRYPTED_SHA256),
    ],
)
def test_file_encrypted(
    in_place_bitflip_encryptor, ransomware_target, file_name, cleartext_hash, encrypted_hash
):
    test_keyboard = ransomware_target / file_name

    assert hash_file(test_keyboard) == cleartext_hash

    in_place_bitflip_encryptor(test_keyboard)

    assert hash_file(test_keyboard) == encrypted_hash


def test_file_encrypted_in_place(in_place_bitflip_encryptor, ransomware_target):
    test_keyboard = ransomware_target / TEST_KEYBOARD_TXT

    expected_inode = os.stat(test_keyboard).st_ino
    in_place_bitflip_encryptor(test_keyboard)
    actual_inode = os.stat(test_keyboard).st_ino

    assert expected_inode == actual_inode


def test_encrypted_file_has_new_extension(ransomware_target):
    test_keyboard = ransomware_target / TEST_KEYBOARD_TXT
    encrypted_test_keyboard = ransomware_target / with_extension(TEST_KEYBOARD_TXT)
    encryptor = InPlaceEncryptor(encrypt_bytes=flip_bits, new_file_extension=EXTENSION)

    encryptor(test_keyboard)

    assert not test_keyboard.exists()
    assert encrypted_test_keyboard.exists()
    assert hash_file(encrypted_test_keyboard) == TEST_KEYBOARD_TXT_ENCRYPTED_SHA256
