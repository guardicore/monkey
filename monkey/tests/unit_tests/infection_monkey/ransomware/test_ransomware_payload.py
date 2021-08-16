from pathlib import PurePosixPath
from unittest.mock import MagicMock

import pytest
from tests.unit_tests.infection_monkey.ransomware.ransomware_target_files import (
    ALL_ZEROS_PDF,
    TEST_KEYBOARD_TXT,
)

from infection_monkey.ransomware.consts import README_FILE_NAME, README_SRC
from infection_monkey.ransomware.ransomware_config import RansomwareConfig
from infection_monkey.ransomware.ransomware_payload import RansomwarePayload


@pytest.fixture
def ransomware_payload(build_ransomware_payload, ransomware_payload_config):
    return build_ransomware_payload(ransomware_payload_config)


@pytest.fixture
def build_ransomware_payload(
    mock_file_encryptor, mock_file_selector, mock_leave_readme, telemetry_messenger_spy
):
    def inner(config):
        return RansomwarePayload(
            config,
            mock_file_encryptor,
            mock_file_selector,
            mock_leave_readme,
            telemetry_messenger_spy,
        )

    return inner


@pytest.fixture
def ransomware_payload_config(ransomware_test_data):
    class RansomwareConfigStub(RansomwareConfig):
        def __init__(self, encryption_enabled, readme_enabled, target_directory):
            self.encryption_enabled = encryption_enabled
            self.readme_enabled = readme_enabled
            self.target_directory = target_directory

    return RansomwareConfigStub(True, False, ransomware_test_data)


@pytest.fixture
def mock_file_encryptor():
    return MagicMock()


@pytest.fixture
def mock_file_selector(ransomware_test_data):
    selected_files = [
        ransomware_test_data / ALL_ZEROS_PDF,
        ransomware_test_data / TEST_KEYBOARD_TXT,
    ]
    return MagicMock(return_value=selected_files)


@pytest.fixture
def mock_leave_readme():
    return MagicMock()


def test_files_selected_from_target_dir(
    ransomware_payload,
    ransomware_payload_config,
    mock_file_selector,
):
    ransomware_payload.run_payload()
    mock_file_selector.assert_called_with(ransomware_payload_config.target_directory)


def test_all_selected_files_encrypted(
    ransomware_test_data, ransomware_payload, mock_file_encryptor
):
    ransomware_payload.run_payload()

    assert mock_file_encryptor.call_count == 2
    mock_file_encryptor.assert_any_call(ransomware_test_data / ALL_ZEROS_PDF)
    mock_file_encryptor.assert_any_call(ransomware_test_data / TEST_KEYBOARD_TXT)


def test_encryption_skipped_if_configured_false(
    build_ransomware_payload, ransomware_payload_config, mock_file_encryptor
):
    ransomware_payload_config.encryption_enabled = False

    ransomware_payload = build_ransomware_payload(ransomware_payload_config)
    ransomware_payload.run_payload()

    assert mock_file_encryptor.call_count == 0


def test_encryption_skipped_if_no_directory(
    build_ransomware_payload, ransomware_payload_config, mock_file_encryptor
):
    ransomware_payload_config.encryption_enabled = True
    ransomware_payload_config.target_directory = None

    ransomware_payload = build_ransomware_payload(ransomware_payload_config)
    ransomware_payload.run_payload()

    assert mock_file_encryptor.call_count == 0


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


def test_telemetry_failure(
    monkeypatch, ransomware_payload_config, mock_leave_readme, telemetry_messenger_spy
):
    file_not_exists = "/file/not/exist"
    ransomware_payload = RansomwarePayload(
        ransomware_payload_config,
        MagicMock(
            side_effect=FileNotFoundError(
                f"[Errno 2] No such file or directory: '{file_not_exists}'"
            )
        ),
        MagicMock(return_value=[PurePosixPath(file_not_exists)]),
        mock_leave_readme,
        telemetry_messenger_spy,
    )

    ransomware_payload.run_payload()
    telem = telemetry_messenger_spy.telemetries[0]

    assert file_not_exists in telem.get_data()["files"][0]["path"]
    assert not telem.get_data()["files"][0]["success"]
    assert "No such file or directory" in telem.get_data()["files"][0]["error"]


def test_readme_false(build_ransomware_payload, ransomware_payload_config, mock_leave_readme):
    ransomware_payload_config.readme_enabled = False
    ransomware_payload = build_ransomware_payload(ransomware_payload_config)

    ransomware_payload.run_payload()
    mock_leave_readme.assert_not_called()


def test_readme_true(
    build_ransomware_payload, ransomware_payload_config, mock_leave_readme, ransomware_test_data
):
    ransomware_payload_config.readme_enabled = True
    ransomware_payload = build_ransomware_payload(ransomware_payload_config)

    ransomware_payload.run_payload()
    mock_leave_readme.assert_called_with(README_SRC, ransomware_test_data / README_FILE_NAME)


def test_no_readme_if_no_directory(
    build_ransomware_payload, ransomware_payload_config, mock_leave_readme
):
    ransomware_payload_config.target_directory = None
    ransomware_payload_config.readme_enabled = True

    ransomware_payload = build_ransomware_payload(ransomware_payload_config)

    ransomware_payload.run_payload()
    mock_leave_readme.assert_not_called()
