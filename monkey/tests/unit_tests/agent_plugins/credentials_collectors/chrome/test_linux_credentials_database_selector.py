from pathlib import Path, PurePath
from unittest.mock import MagicMock

import pytest

pwd = pytest.importorskip("pwd")
# we need to check if `pwd` can be imported before importing the selector
from agent_plugins.credentials_collectors.chrome.src.linux_credentials_database_selector import (  # noqa:E402, E501
    LinuxCredentialsDatabaseSelector,
)

USERNAME_1 = "user1"
USERNAME_2 = "user2"

GOOGLE_CHROME_PATH = ".config/google-chrome"
BRAVE_PATH = ".config/BraveSoftware/Brave-Browser"
SLIMJET_PATH = ".config/slimjet"


@pytest.fixture
def linux_credentials_database_selector() -> LinuxCredentialsDatabaseSelector:
    return LinuxCredentialsDatabaseSelector()


def test_linux_selector__pwd_exception(monkeypatch, linux_credentials_database_selector):
    mock_pwd = MagicMock()
    mock_pwd.getpwall = MagicMock(side_effect=Exception)
    monkeypatch.setattr(
        "agent_plugins.credentials_collectors.chrome.src.linux_credentials_database_selector.pwd",
        mock_pwd,
    )

    actual_login_database_paths = linux_credentials_database_selector()
    assert actual_login_database_paths == []


@pytest.fixture
def place_browser_files(tmp_path):
    inaccessible_user_2_dir_chrome = tmp_path / "home" / USERNAME_2 / f"{GOOGLE_CHROME_PATH}"
    inaccessible_user_2_dir_chrome.mkdir(parents=True)
    inaccessible_user_2_dir_chrome.chmod(mode=0o000)

    inaccessible_user_2_dir_brave = tmp_path / "home" / USERNAME_2 / f"{BRAVE_PATH}/Default"
    inaccessible_user_2_dir_brave.mkdir(parents=True)
    (inaccessible_user_2_dir_brave / "Login Data").touch(mode=0o000)

    user_1_dir_chrome = tmp_path / "home" / USERNAME_1 / f"{GOOGLE_CHROME_PATH}/Default"
    user_1_dir_chrome.mkdir(parents=True)
    (user_1_dir_chrome / "Login Data").touch()

    user_1_dir_brave = tmp_path / "home" / USERNAME_1 / f"{BRAVE_PATH}/Default"
    user_1_dir_brave.mkdir(parents=True)
    (user_1_dir_brave / "Login Data").touch()

    user_2_dir_slimjet = tmp_path / "home" / USERNAME_2 / f"{SLIMJET_PATH}"
    user_2_dir_slimjet.mkdir(parents=True)
    (user_2_dir_slimjet / "Login Data").touch()

    yield

    # Set these permissions so that pytest can clean up the directory
    inaccessible_user_2_dir_chrome.chmod(0o700)
    inaccessible_user_2_dir_brave.chmod(0o700)


@pytest.fixture
def patch_pwd_getpwall(monkeypatch, place_browser_files, tmp_path: Path):
    pwd_structs = [
        pwd.struct_passwd(  # type: ignore[attr-defined]
            [
                USERNAME_1,
                "x",
                4,
                65534,
                "sync",
                tmp_path / f"home/{USERNAME_1}",
                "/bin/sync",
            ]
        ),
        pwd.struct_passwd(  # type: ignore[attr-defined]
            [
                USERNAME_2,
                "x",
                4,
                65534,
                "sync",
                tmp_path / f"home/{USERNAME_2}",
                "/bin/sync",
            ]
        ),
    ]
    mock_pwd = MagicMock()
    mock_pwd.getpwall = MagicMock(return_value=pwd_structs)
    monkeypatch.setattr(
        "agent_plugins.credentials_collectors.chrome.src.linux_credentials_database_selector.pwd",
        mock_pwd,
    )


@pytest.fixture
def patch_env_home(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("HOME", str(tmp_path / "home" / USERNAME_1))


@pytest.fixture
def expected_login_database_paths(tmp_path: Path):
    return [
        PurePath(f"{tmp_path}/home/{USERNAME_1}/{GOOGLE_CHROME_PATH}/Default/Login Data"),
        PurePath(f"{tmp_path}/home/{USERNAME_1}/{BRAVE_PATH}/Default/Login Data"),
        PurePath(f"{tmp_path}/home/{USERNAME_2}/{SLIMJET_PATH}/Login Data"),
    ]


def test_linux_credentials_database_selector(
    patch_pwd_getpwall,
    patch_env_home,
    linux_credentials_database_selector,
    expected_login_database_paths,
):
    actual_login_database_paths = linux_credentials_database_selector()

    assert len(actual_login_database_paths) == len(expected_login_database_paths)
    assert actual_login_database_paths == expected_login_database_paths


@pytest.mark.parametrize(
    "method, error",
    [
        ("is_file", Exception),
        ("is_file", PermissionError),
        ("is_dir", Exception),
        ("is_dir", PermissionError),
    ],
)
def test_linux_credentials_database_selector__exception(
    monkeypatch, patch_pwd_getpwall, linux_credentials_database_selector, error, method
):
    def mock_method(path):
        raise error()

    monkeypatch.setattr(
        f"agent_plugins.credentials_collectors.chrome.src.linux_credentials_database_selector.Path.{method}",  # noqa: E501
        mock_method,
    )
    actual_login_database_paths = linux_credentials_database_selector()

    assert actual_login_database_paths == []
