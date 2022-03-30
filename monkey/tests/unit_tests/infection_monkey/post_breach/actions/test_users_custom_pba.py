from unittest.mock import MagicMock

import pytest

from infection_monkey.post_breach.custom_pba.custom_pba import CustomPBA

MONKEY_DIR_PATH = "/dir/to/monkey/"
CUSTOM_LINUX_CMD = "command-for-linux"
CUSTOM_LINUX_FILENAME = "filename-for-linux"
CUSTOM_WINDOWS_CMD = "command-for-windows"
CUSTOM_WINDOWS_FILENAME = "filename-for-windows"
CUSTOM_SERVER = "10.10.10.10:5000"


@pytest.fixture(autouse=True)
def fake_monkey_dir_path(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.post_breach.custom_pba.custom_pba.get_monkey_dir_path",
        lambda: MONKEY_DIR_PATH,
    )


@pytest.fixture
def set_os_linux(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.post_breach.custom_pba.custom_pba.is_windows_os",
        lambda: False,
    )


@pytest.fixture
def set_os_windows(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.post_breach.custom_pba.custom_pba.is_windows_os",
        lambda: True,
    )


@pytest.fixture
def fake_custom_pba_linux_options():
    return {
        "linux_command": CUSTOM_LINUX_CMD,
        "linux_filename": CUSTOM_LINUX_FILENAME,
        "windows_command": "",
        "windows_filename": "",
        # Current server is used for attack telemetry
        "current_server": CUSTOM_SERVER,
    }


def test_command_linux_custom_file_and_cmd(fake_custom_pba_linux_options, set_os_linux):
    pba = CustomPBA(MagicMock())
    pba._set_options(fake_custom_pba_linux_options)
    expected_command = f"cd {MONKEY_DIR_PATH} ; {CUSTOM_LINUX_CMD}"
    assert pba.command == expected_command
    assert pba.filename == CUSTOM_LINUX_FILENAME


@pytest.fixture
def fake_custom_pba_windows_options():
    return {
        "linux_command": "",
        "linux_filename": "",
        "windows_command": CUSTOM_WINDOWS_CMD,
        "windows_filename": CUSTOM_WINDOWS_FILENAME,
        # Current server is used for attack telemetry
        "current_server": CUSTOM_SERVER,
    }


def test_command_windows_custom_file_and_cmd(fake_custom_pba_windows_options, set_os_windows):

    pba = CustomPBA(MagicMock())
    pba._set_options(fake_custom_pba_windows_options)
    expected_command = f"cd {MONKEY_DIR_PATH} & {CUSTOM_WINDOWS_CMD}"
    assert pba.command == expected_command
    assert pba.filename == CUSTOM_WINDOWS_FILENAME


@pytest.fixture
def fake_options_files_only():
    return {
        "linux_command": "",
        "linux_filename": CUSTOM_LINUX_FILENAME,
        "windows_command": "",
        "windows_filename": CUSTOM_WINDOWS_FILENAME,
        # Current server is used for attack telemetry
        "current_server": CUSTOM_SERVER,
    }


@pytest.mark.parametrize("os", [set_os_linux, set_os_windows])
def test_files_only(fake_options_files_only, os):
    pba = CustomPBA(MagicMock())
    pba._set_options(fake_options_files_only)
    assert pba.command == ""


@pytest.fixture
def fake_options_commands_only():
    return {
        "linux_command": CUSTOM_LINUX_CMD,
        "linux_filename": "",
        "windows_command": CUSTOM_WINDOWS_CMD,
        "windows_filename": "",
        # Current server is used for attack telemetry
        "current_server": CUSTOM_SERVER,
    }


def test_commands_only(fake_options_commands_only, set_os_linux):
    pba = CustomPBA(MagicMock())
    pba._set_options(fake_options_commands_only)
    assert pba.command == CUSTOM_LINUX_CMD
    assert pba.filename == ""


def test_commands_only_windows(fake_options_commands_only, set_os_windows):
    pba = CustomPBA(MagicMock())
    pba._set_options(fake_options_commands_only)
    assert pba.command == CUSTOM_WINDOWS_CMD
    assert pba.filename == ""
