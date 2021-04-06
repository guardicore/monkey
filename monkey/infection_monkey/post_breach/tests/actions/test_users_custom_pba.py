import pytest

from infection_monkey.post_breach.actions.users_custom_pba import (
    DIR_CHANGE_LINUX, DIR_CHANGE_WINDOWS, UsersPBA)

MONKEY_DIR_PATH = "/dir/to/monkey/"
CUSTOM_LINUX_CMD = "command-for-linux"
CUSTOM_LINUX_FILENAME = "filename-for-linux"
CUSTOM_WINDOWS_CMD = "command-for-windows"
CUSTOM_WINDOWS_FILENAME = "filename-for-windows"


@pytest.fixture
def fake_monkey_dir_path(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.post_breach.actions.users_custom_pba.get_monkey_dir_path",
        lambda: MONKEY_DIR_PATH,
    )


@pytest.fixture
def set_os_linux(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.post_breach.actions.users_custom_pba.is_windows_os",
        lambda: False,
    )


@pytest.fixture
def set_os_windows(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.post_breach.actions.users_custom_pba.is_windows_os",
        lambda: True,
    )


@pytest.fixture
def mock_UsersPBA_linux_custom_file_and_cmd(
    set_os_linux, fake_monkey_dir_path, monkeypatch
):
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.custom_PBA_linux_cmd",
        CUSTOM_LINUX_CMD,
    )
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.PBA_linux_filename",
        CUSTOM_LINUX_FILENAME,
    )
    return UsersPBA()


def test_command_linux_custom_file_and_cmd(
    mock_UsersPBA_linux_custom_file_and_cmd,
):
    expected_command = f"cd {MONKEY_DIR_PATH} ; {CUSTOM_LINUX_CMD}"
    assert mock_UsersPBA_linux_custom_file_and_cmd.command == expected_command


@pytest.fixture
def mock_UsersPBA_windows_custom_file_and_cmd(
    set_os_windows, fake_monkey_dir_path, monkeypatch
):
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.custom_PBA_windows_cmd",
        CUSTOM_WINDOWS_CMD,
    )
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.PBA_windows_filename",
        CUSTOM_WINDOWS_FILENAME,
    )
    return UsersPBA()


def test_command_windows_custom_file_and_cmd(
    mock_UsersPBA_windows_custom_file_and_cmd,
):
    expected_command = f"cd {MONKEY_DIR_PATH} & {CUSTOM_WINDOWS_CMD}"
    assert mock_UsersPBA_windows_custom_file_and_cmd.command == expected_command


@pytest.fixture
def mock_UsersPBA_linux_custom_file(set_os_linux, fake_monkey_dir_path, monkeypatch):

    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.custom_PBA_linux_cmd", None
    )
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.PBA_linux_filename",
        CUSTOM_LINUX_FILENAME,
    )
    return UsersPBA()


def test_command_linux_custom_file(mock_UsersPBA_linux_custom_file):
    expected_command = ""
    assert mock_UsersPBA_linux_custom_file.command == expected_command


@pytest.fixture
def mock_UsersPBA_windows_custom_file(
    set_os_windows, fake_monkey_dir_path, monkeypatch
):

    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.custom_PBA_windows_cmd", None
    )
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.PBA_windows_filename",
        CUSTOM_WINDOWS_FILENAME,
    )
    return UsersPBA()


def test_command_windows_custom_file(mock_UsersPBA_windows_custom_file):
    expected_command = ""
    assert mock_UsersPBA_windows_custom_file.command == expected_command


@pytest.fixture
def mock_UsersPBA_linux_custom_cmd(set_os_linux, fake_monkey_dir_path, monkeypatch):

    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.custom_PBA_linux_cmd",
        CUSTOM_LINUX_CMD,
    )
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.PBA_linux_filename", None
    )
    return UsersPBA()


def test_command_linux_custom_cmd(mock_UsersPBA_linux_custom_cmd):
    expected_command = CUSTOM_LINUX_CMD
    assert mock_UsersPBA_linux_custom_cmd.command == expected_command


@pytest.fixture
def mock_UsersPBA_windows_custom_cmd(set_os_windows, fake_monkey_dir_path, monkeypatch):

    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.custom_PBA_windows_cmd",
        CUSTOM_WINDOWS_CMD,
    )
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.PBA_windows_filename", None
    )
    return UsersPBA()


def test_command_windows_custom_cmd(mock_UsersPBA_windows_custom_cmd):
    expected_command = CUSTOM_WINDOWS_CMD
    assert mock_UsersPBA_windows_custom_cmd.command == expected_command
