import pytest

from infection_monkey.post_breach.actions.users_custom_pba import (
    DEFAULT_LINUX_COMMAND, DEFAULT_WINDOWS_COMMAND, DIR_CHANGE_LINUX,
    DIR_CHANGE_WINDOWS, UsersPBA)

MONKEY_DIR_PATH = "/dir/to/monkey/"
CUSTOM_LINUX_CMD_SEPARATE = "command-for-linux"
CUSTOM_LINUX_FILENAME = "filename-for-linux"
CUSTOM_LINUX_CMD_RELATED = f"command-with-{CUSTOM_LINUX_FILENAME}"
CUSTOM_WINDOWS_CMD_SEPARATE = "command-for-windows"
CUSTOM_WINDOWS_FILENAME = "filename-for-windows"
CUSTOM_WINDOWS_CMD_RELATED = f"command-with-{CUSTOM_WINDOWS_FILENAME}"


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
def mock_UsersPBA_linux_custom_file_and_cmd_separate(
    set_os_linux, fake_monkey_dir_path, monkeypatch
):
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.custom_PBA_linux_cmd",
        CUSTOM_LINUX_CMD_SEPARATE,
    )
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.PBA_linux_filename",
        CUSTOM_LINUX_FILENAME,
    )
    return UsersPBA()


def test_command_list_linux_custom_file_and_cmd_separate(
    mock_UsersPBA_linux_custom_file_and_cmd_separate,
):
    expected_command_list = [
        f"cd {MONKEY_DIR_PATH} ; {CUSTOM_LINUX_CMD_SEPARATE}",
        f"chmod +x {MONKEY_DIR_PATH}{CUSTOM_LINUX_FILENAME} ; {MONKEY_DIR_PATH}{CUSTOM_LINUX_FILENAME} ; " +
        f"rm {MONKEY_DIR_PATH}{CUSTOM_LINUX_FILENAME}",
    ]
    assert (
        mock_UsersPBA_linux_custom_file_and_cmd_separate.command_list
        == expected_command_list
    )


@pytest.fixture
def mock_UsersPBA_windows_custom_file_and_cmd_separate(
    set_os_windows, fake_monkey_dir_path, monkeypatch
):
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.custom_PBA_windows_cmd",
        CUSTOM_WINDOWS_CMD_SEPARATE,
    )
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.PBA_windows_filename",
        CUSTOM_WINDOWS_FILENAME,
    )
    return UsersPBA()


def test_command_list_windows_custom_file_and_cmd_separate(
    mock_UsersPBA_windows_custom_file_and_cmd_separate,
):
    expected_command_list = [
        f"cd {MONKEY_DIR_PATH} & {CUSTOM_WINDOWS_CMD_SEPARATE}",
        f"{MONKEY_DIR_PATH}{CUSTOM_WINDOWS_FILENAME} & del {MONKEY_DIR_PATH}{CUSTOM_WINDOWS_FILENAME}",
    ]
    assert (
        mock_UsersPBA_windows_custom_file_and_cmd_separate.command_list
        == expected_command_list
    )


@pytest.fixture
def mock_UsersPBA_linux_custom_file_and_cmd_related(
    set_os_linux, fake_monkey_dir_path, monkeypatch
):
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.custom_PBA_linux_cmd",
        CUSTOM_LINUX_CMD_RELATED,
    )
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.PBA_linux_filename",
        CUSTOM_LINUX_FILENAME,
    )
    return UsersPBA()


def test_command_list_linux_custom_file_and_cmd_related(
    mock_UsersPBA_linux_custom_file_and_cmd_related,
):
    expected_command_list = [f"cd {MONKEY_DIR_PATH} ; {CUSTOM_LINUX_CMD_RELATED}"]
    assert (
        mock_UsersPBA_linux_custom_file_and_cmd_related.command_list
        == expected_command_list
    )


@pytest.fixture
def mock_UsersPBA_windows_custom_file_and_cmd_related(
    set_os_windows, fake_monkey_dir_path, monkeypatch
):

    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.custom_PBA_windows_cmd",
        CUSTOM_WINDOWS_CMD_RELATED,
    )
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.PBA_windows_filename",
        CUSTOM_WINDOWS_FILENAME,
    )
    return UsersPBA()


def test_command_list_windows_custom_file_and_cmd_related(
    mock_UsersPBA_windows_custom_file_and_cmd_related,
):
    expected_command_list = [
        f"cd {MONKEY_DIR_PATH} & {CUSTOM_WINDOWS_CMD_RELATED}",
    ]
    assert (
        mock_UsersPBA_windows_custom_file_and_cmd_related.command_list
        == expected_command_list
    )


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


def test_command_list_linux_custom_file(mock_UsersPBA_linux_custom_file):
    expected_command_list = [
        f"chmod +x {MONKEY_DIR_PATH}{CUSTOM_LINUX_FILENAME} ; {MONKEY_DIR_PATH}{CUSTOM_LINUX_FILENAME} ; " +
        f"rm {MONKEY_DIR_PATH}{CUSTOM_LINUX_FILENAME}"
    ]

    assert mock_UsersPBA_linux_custom_file.command_list == expected_command_list


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


def test_command_list_windows_custom_file(mock_UsersPBA_windows_custom_file):
    expected_command_list = [
        f"{MONKEY_DIR_PATH}{CUSTOM_WINDOWS_FILENAME} & del {MONKEY_DIR_PATH}{CUSTOM_WINDOWS_FILENAME}",
    ]
    assert mock_UsersPBA_windows_custom_file.command_list == expected_command_list


@pytest.fixture
def mock_UsersPBA_linux_custom_cmd(set_os_linux, fake_monkey_dir_path, monkeypatch):

    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.custom_PBA_linux_cmd",
        CUSTOM_LINUX_CMD_SEPARATE,
    )
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.PBA_linux_filename", None
    )
    return UsersPBA()


def test_command_list_linux_custom_cmd(mock_UsersPBA_linux_custom_cmd):
    expected_command_list = [CUSTOM_LINUX_CMD_SEPARATE]
    assert mock_UsersPBA_linux_custom_cmd.command_list == expected_command_list


@pytest.fixture
def mock_UsersPBA_windows_custom_cmd(set_os_windows, fake_monkey_dir_path, monkeypatch):

    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.custom_PBA_windows_cmd",
        CUSTOM_WINDOWS_CMD_SEPARATE,
    )
    monkeypatch.setattr(
        "infection_monkey.config.WormConfiguration.PBA_windows_filename", None
    )
    return UsersPBA()


def test_command_list_windows_custom_cmd(mock_UsersPBA_windows_custom_cmd):
    expected_command_list = [CUSTOM_WINDOWS_CMD_SEPARATE]
    assert mock_UsersPBA_windows_custom_cmd.command_list == expected_command_list
