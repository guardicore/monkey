from tests.unit_tests.infection_monkey.ransomware.ransomware_target_files import (
    ALL_ZEROS_PDF,
    ALL_ZEROS_PDF_CLEARTEXT_SHA256,
    ALL_ZEROS_PDF_ENCRYPTED_SHA256,
    TEST_KEYBOARD_TXT,
    TEST_KEYBOARD_TXT_CLEARTEXT_SHA256,
    TEST_KEYBOARD_TXT_ENCRYPTED_SHA256,
)
from tests.utils import hash_file

from infection_monkey.ransomware.ransomware_bitflip_encryptor import RansomwareBitflipEncryptor

EXTENSION = ".new"


def with_extension(filename):
    return f"{filename}{EXTENSION}"


def test_listed_files_encrypted(ransomware_target):
    orig_all_zeros = ransomware_target / ALL_ZEROS_PDF
    orig_test_keyboard = ransomware_target / TEST_KEYBOARD_TXT
    file_list = [orig_all_zeros, orig_test_keyboard]

    assert hash_file(file_list[0]) == ALL_ZEROS_PDF_CLEARTEXT_SHA256
    assert hash_file(file_list[1]) == TEST_KEYBOARD_TXT_CLEARTEXT_SHA256

    encryptor = RansomwareBitflipEncryptor(EXTENSION)
    encryptor.encrypt_files(file_list)

    assert hash_file(with_extension(orig_all_zeros)) == ALL_ZEROS_PDF_ENCRYPTED_SHA256
    assert hash_file(with_extension(orig_test_keyboard)) == TEST_KEYBOARD_TXT_ENCRYPTED_SHA256


def test_encrypted_files_in_results(ransomware_target):
    orig_all_zeros = ransomware_target / ALL_ZEROS_PDF
    orig_test_keyboard = ransomware_target / TEST_KEYBOARD_TXT
    file_list = [orig_all_zeros, orig_test_keyboard]

    encryptor = RansomwareBitflipEncryptor(EXTENSION)
    results = encryptor.encrypt_files(file_list)

    assert len(results) == 2
    assert (orig_all_zeros, None) in results
    assert (orig_test_keyboard, None) in results


def test_file_not_found(ransomware_target):
    all_zeros = ransomware_target / ALL_ZEROS_PDF
    file_list = [all_zeros]

    all_zeros.unlink()

    encryptor = RansomwareBitflipEncryptor(EXTENSION)

    results = encryptor.encrypt_files(file_list)

    assert len(results) == 1
    assert "No such file or directory" in str(results[0][1])
