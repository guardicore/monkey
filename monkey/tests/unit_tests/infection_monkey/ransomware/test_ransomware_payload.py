import os

import pytest
from tests.unit_tests.infection_monkey.ransomware.ransomware_target_files import (
    ALL_ZEROS_PDF,
    ALL_ZEROS_PDF_CLEARTEXT_SHA256,
    ALL_ZEROS_PDF_ENCRYPTED_SHA256,
    ALREADY_ENCRYPTED_TXT_M0NK3Y,
    ALREADY_ENCRYPTED_TXT_M0NK3Y_CLEARTEXT_SHA256,
    HELLO_TXT,
    HELLO_TXT_CLEARTEXT_SHA256,
    SHORTCUT_LNK,
    SHORTCUT_LNK_CLEARTEXT_SHA256,
    SUBDIR,
    TEST_KEYBOARD_TXT,
    TEST_KEYBOARD_TXT_CLEARTEXT_SHA256,
    TEST_KEYBOARD_TXT_ENCRYPTED_SHA256,
    TEST_LIB_DLL,
    TEST_LIB_DLL_CLEARTEXT_SHA256,
)
from tests.utils import hash_file, is_user_admin

from infection_monkey.ransomware.ransomware_payload import EXTENSION, RansomewarePayload


def with_extension(filename):
    return f"{filename}{EXTENSION}"


@pytest.fixture
def ransomware_payload_config(ransomware_target):
    return {"linux_dir": str(ransomware_target), "windows_dir": str(ransomware_target)}


@pytest.fixture
def ransomware_payload(ransomware_payload_config):
    return RansomewarePayload(ransomware_payload_config)


def test_file_with_excluded_extension_not_encrypted(ransomware_target, ransomware_payload):
    ransomware_payload.run_payload()

    assert hash_file(ransomware_target / TEST_LIB_DLL) == TEST_LIB_DLL_CLEARTEXT_SHA256


def test_shortcut_not_encrypted(ransomware_target, ransomware_payload):
    ransomware_payload.run_payload()

    assert hash_file(ransomware_target / SHORTCUT_LNK) == SHORTCUT_LNK_CLEARTEXT_SHA256


@pytest.mark.skipif(
    os.name == "nt" and not is_user_admin(), reason="Test requires admin rights on Windows"
)
def test_symlink_not_encrypted(ransomware_target, ransomware_payload):
    SYMLINK = "symlink.pdf"
    link_path = ransomware_target / SYMLINK
    link_path.symlink_to(ransomware_target / TEST_LIB_DLL)

    ransomware_payload.run_payload()

    assert hash_file(ransomware_target / SYMLINK) == TEST_LIB_DLL_CLEARTEXT_SHA256


def test_encryption_not_recursive(ransomware_target, ransomware_payload):
    ransomware_payload.run_payload()

    assert hash_file(ransomware_target / SUBDIR / HELLO_TXT) == HELLO_TXT_CLEARTEXT_SHA256


def test_all_files_with_included_extension_encrypted(ransomware_target, ransomware_payload):
    assert hash_file(ransomware_target / ALL_ZEROS_PDF) == ALL_ZEROS_PDF_CLEARTEXT_SHA256
    assert hash_file(ransomware_target / TEST_KEYBOARD_TXT) == TEST_KEYBOARD_TXT_CLEARTEXT_SHA256

    ransomware_payload.run_payload()

    assert (
        hash_file(ransomware_target / with_extension(ALL_ZEROS_PDF))
        == ALL_ZEROS_PDF_ENCRYPTED_SHA256
    )
    assert (
        hash_file(ransomware_target / with_extension(TEST_KEYBOARD_TXT))
        == TEST_KEYBOARD_TXT_ENCRYPTED_SHA256
    )


def test_file_encrypted_in_place(ransomware_target, ransomware_payload):
    expected_all_zeros_inode = os.stat(ransomware_target / ALL_ZEROS_PDF).st_ino
    expected_test_keyboard_inode = os.stat(ransomware_target / TEST_KEYBOARD_TXT).st_ino

    ransomware_payload.run_payload()

    actual_all_zeros_inode = os.stat(ransomware_target / with_extension(ALL_ZEROS_PDF)).st_ino
    actual_test_keyboard_inode = os.stat(
        ransomware_target / with_extension(TEST_KEYBOARD_TXT)
    ).st_ino

    assert expected_all_zeros_inode == actual_all_zeros_inode
    assert expected_test_keyboard_inode == actual_test_keyboard_inode


def test_encryption_reversible(ransomware_target, ransomware_payload):
    orig_path = ransomware_target / TEST_KEYBOARD_TXT
    new_path = ransomware_target / with_extension(TEST_KEYBOARD_TXT)
    assert hash_file(orig_path) == TEST_KEYBOARD_TXT_CLEARTEXT_SHA256

    ransomware_payload.run_payload()
    assert hash_file(new_path) == TEST_KEYBOARD_TXT_ENCRYPTED_SHA256

    new_path.rename(orig_path)
    ransomware_payload.run_payload()
    assert (
        hash_file(ransomware_target / with_extension(TEST_KEYBOARD_TXT))
        == TEST_KEYBOARD_TXT_CLEARTEXT_SHA256
    )


def test_skip_already_encrypted_file(ransomware_target, ransomware_payload):
    ransomware_payload.run_payload()

    assert not (ransomware_target / with_extension(ALREADY_ENCRYPTED_TXT_M0NK3Y)).exists()
    assert (
        hash_file(ransomware_target / ALREADY_ENCRYPTED_TXT_M0NK3Y)
        == ALREADY_ENCRYPTED_TXT_M0NK3Y_CLEARTEXT_SHA256
    )
