import os

import pytest
from tests.utils import hash_file, is_user_admin

from infection_monkey.ransomware.ransomware_payload import EXTENSION, RansomewarePayload

SUBDIR = "subdir"
ALL_ZEROS_PDF = "all_zeros.pdf"
ALREADY_ENCRYPTED_TXT_M0NK3Y = "already_encrypted.txt.m0nk3y"
HELLO_TXT = "hello.txt"
SHORTCUT_LNK = "shortcut.lnk"
TEST_KEYBOARD_TXT = "test_keyboard.txt"
TEST_LIB_DLL = "test_lib.dll"

ALL_ZEROS_PDF_CLEARTEXT_SHA256 = "ab3df617aaa3140f04dc53f65b5446f34a6b2bdbb1f7b78db8db4d067ba14db9"
ALREADY_ENCRYPTED_TXT_M0NK3Y_CLEARTEXT_SHA256 = (
    "ff5e58498962ab8bd619d3a9cd24b9298e7efc25b4967b1ce3f03b0e6de2aa7a"
)
HELLO_TXT_CLEARTEXT_SHA256 = "0ba904eae8773b70c75333db4de2f3ac45a8ad4ddba1b242f0b3cfc199391dd8"
SHORTCUT_LNK_CLEARTEXT_SHA256 = "5069c8b7c3c70fad55bf0f0790de787080b1b4397c4749affcd3e570ff53aad9"
TEST_KEYBOARD_TXT_CLEARTEXT_SHA256 = (
    "9d1a38784b7eefef6384bfc4b89048017db840adace11504a947016072750b2b"
)
TEST_LIB_DLL_CLEARTEXT_SHA256 = "0922d3132f2378edf313b8c2b6609a2548879911686994ca45fc5c895a7e91b1"

ALL_ZEROS_PDF_ENCRYPTED_SHA256 = "779c176e820dbdaf643419232cb4d2760360c8633d6fe209cf706707db799b4d"
TEST_KEYBOARD_TXT_ENCRYPTED_SHA256 = (
    "80701f3694abdd25ef3df7166b3fc5189b2afb4df32f7d5adbfed61ad07b9cd5"
)


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


def test_file_with_included_extension_encrypted(ransomware_target, ransomware_payload):
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
