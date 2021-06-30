import os
from pathlib import Path, PurePosixPath

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

from infection_monkey.ransomware import ransomware_payload as ransomware_payload_module
from infection_monkey.ransomware.ransomware_payload import EXTENSION, README_DEST, RansomwarePayload


def with_extension(filename):
    return f"{filename}{EXTENSION}"


@pytest.fixture
def ransomware_payload_config(ransomware_target):
    return {
        "encryption": {
            "enabled": True,
            "directories": {
                "linux_dir": str(ransomware_target),
                "windows_dir": str(ransomware_target),
            },
        },
        "other_behaviors": {"readme": False},
    }


@pytest.fixture
def ransomware_payload(ransomware_payload_config, telemetry_messenger_spy):
    return RansomwarePayload(ransomware_payload_config, telemetry_messenger_spy)


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
    expected_test_keyboard_inode = os.stat(ransomware_target / TEST_KEYBOARD_TXT).st_ino

    ransomware_payload.run_payload()

    actual_test_keyboard_inode = os.stat(
        ransomware_target / with_extension(TEST_KEYBOARD_TXT)
    ).st_ino

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


def test_encryption_skipped_if_configured_false(
    ransomware_payload_config, ransomware_target, telemetry_messenger_spy
):
    ransomware_payload_config["encryption"]["enabled"] = False

    ransomware_payload = RansomwarePayload(ransomware_payload_config, telemetry_messenger_spy)
    ransomware_payload.run_payload()

    assert hash_file(ransomware_target / ALL_ZEROS_PDF) == ALL_ZEROS_PDF_CLEARTEXT_SHA256
    assert hash_file(ransomware_target / TEST_KEYBOARD_TXT) == TEST_KEYBOARD_TXT_CLEARTEXT_SHA256


def test_telemetry_success(ransomware_payload, telemetry_messenger_spy):
    ransomware_payload.run_payload()

    assert len(telemetry_messenger_spy.telemetries) == 2
    telem_1 = telemetry_messenger_spy.telemetries[0]
    telem_2 = telemetry_messenger_spy.telemetries[1]

    assert ALL_ZEROS_PDF in telem_1.get_data()["files"][0]["path"]
    assert telem_1.get_data()["files"][0]["success"]
    assert telem_1.get_data()["files"][0]["error"] == ""
    assert TEST_KEYBOARD_TXT in telem_2.get_data()["files"][0]["path"]
    assert telem_2.get_data()["files"][0]["success"]
    assert telem_2.get_data()["files"][0]["error"] == ""


def test_telemetry_failure(monkeypatch, ransomware_payload, telemetry_messenger_spy):
    monkeypatch.setattr(
        ransomware_payload_module,
        "select_production_safe_target_files",
        lambda a, b: [PurePosixPath("/file/not/exist")],
    ),

    ransomware_payload.run_payload()
    telem_1 = telemetry_messenger_spy.telemetries[0]

    assert "/file/not/exist" in telem_1.get_data()["files"][0]["path"]
    assert not telem_1.get_data()["files"][0]["success"]
    assert "No such file or directory" in telem_1.get_data()["files"][0]["error"]


def test_readme_false(ransomware_payload_config, ransomware_target, telemetry_messenger_spy):
    ransomware_payload_config["other_behaviors"]["readme"] = False
    ransomware_payload = RansomwarePayload(ransomware_payload_config, telemetry_messenger_spy)

    ransomware_payload.run_payload()
    assert not Path(ransomware_target / README_DEST).exists()


def test_readme_true(ransomware_payload_config, ransomware_target, telemetry_messenger_spy):
    ransomware_payload_config["other_behaviors"]["readme"] = True
    ransomware_payload = RansomwarePayload(ransomware_payload_config, telemetry_messenger_spy)

    ransomware_payload.run_payload()
    assert Path(ransomware_target / README_DEST).exists()
