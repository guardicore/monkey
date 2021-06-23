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
    file_list = [ransomware_target / ALL_ZEROS_PDF, ransomware_target / TEST_KEYBOARD_TXT]

    assert hash_file(file_list[0]) == ALL_ZEROS_PDF_CLEARTEXT_SHA256
    assert hash_file(file_list[1]) == TEST_KEYBOARD_TXT_CLEARTEXT_SHA256

    encryptor = RansomwareBitflipEncryptor(".new")
    encryptor.encrypt_files(file_list)

    assert hash_file(with_extension(file_list[0])) == ALL_ZEROS_PDF_ENCRYPTED_SHA256
    assert hash_file(with_extension(file_list[1])) == TEST_KEYBOARD_TXT_ENCRYPTED_SHA256
