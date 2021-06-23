import os

from tests.unit_tests.infection_monkey.ransomware.ransomware_target_files import (
    TEST_KEYBOARD_TXT,
    TEST_KEYBOARD_TXT_CLEARTEXT_SHA256,
    TEST_KEYBOARD_TXT_ENCRYPTED_SHA256,
)
from tests.utils import hash_file

from infection_monkey.ransomware.ransomware_bitflip_encryptor import RansomwareBitflipEncryptor


def test_file_encrypted(ransomware_target):
    test_keyboard = ransomware_target / TEST_KEYBOARD_TXT

    assert hash_file(test_keyboard) == TEST_KEYBOARD_TXT_CLEARTEXT_SHA256

    encryptor = RansomwareBitflipEncryptor(chunk_size=64)
    encryptor.encrypt_file_in_place(test_keyboard)

    assert hash_file(test_keyboard) == TEST_KEYBOARD_TXT_ENCRYPTED_SHA256


def test_file_encrypted_in_place(ransomware_target):
    test_keyboard = ransomware_target / TEST_KEYBOARD_TXT

    expected_inode = os.stat(test_keyboard).st_ino

    encryptor = RansomwareBitflipEncryptor(chunk_size=64)
    encryptor.encrypt_file_in_place(test_keyboard)

    actual_inode = os.stat(test_keyboard).st_ino

    assert expected_inode == actual_inode
