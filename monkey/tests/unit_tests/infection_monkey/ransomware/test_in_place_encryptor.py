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


@pytest.fixture(scope="module")
def in_place_bitflip_encryptor():
    return InPlaceEncryptor(flip_bits, 64)


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
