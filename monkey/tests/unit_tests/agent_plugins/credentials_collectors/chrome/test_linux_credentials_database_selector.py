from pathlib import Path
from unittest.mock import MagicMock

import pytest
from agent_plugins.credentials_collectors.chrome.src.browser_credentials_database_path import (
    BrowserCredentialsDatabasePath,
)

pwd = pytest.importorskip("pwd")
# we need to check if `pwd` can be imported before importing the selector
from agent_plugins.credentials_collectors.chrome.src.linux_credentials_database_selector import (  # noqa:E402, E501
    DEFAULT_MASTER_KEY,
    LinuxCredentialsDatabaseSelector,
)

USERNAME_1 = "user1"
USERNAME_2 = "user2"

GOOGLE_CHROME_PATH = ".config/google-chrome"
CHROMIUM_PATH = ".config/chromium"


@pytest.fixture
def linux_credentials_database_selector() -> LinuxCredentialsDatabaseSelector:
    return LinuxCredentialsDatabaseSelector()


def test_linux_selector__pwd_exception(monkeypatch, linux_credentials_database_selector):
    mock_pwd = MagicMock()
    mock_pwd.getpwall = MagicMock(side_effect=PermissionError)
    monkeypatch.setattr(
        "agent_plugins.credentials_collectors.chrome.src.linux_credentials_database_selector.pwd",
        mock_pwd,
    )

    actual_login_database_paths = linux_credentials_database_selector()
    assert list(actual_login_database_paths) == []


@pytest.fixture
def place_browser_files(tmp_path):
    user_1_dir_chrome = tmp_path / "home" / USERNAME_1 / f"{GOOGLE_CHROME_PATH}/Default"
    user_1_dir_chrome.mkdir(parents=True)
    (user_1_dir_chrome / "Login Data").touch()

    user_2_dir_chrome = tmp_path / "home" / USERNAME_2 / f"{GOOGLE_CHROME_PATH}/Default"
    user_2_dir_chrome.mkdir(parents=True)
    (user_2_dir_chrome / "Login Data").touch()

    user_2_dir_chromium = tmp_path / "home" / USERNAME_2 / f"{CHROMIUM_PATH}"
    user_2_dir_chromium.mkdir(parents=True)
    (user_2_dir_chromium / "Login Data").touch()

    yield


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
def expected_login_database_paths(tmp_path: Path):
    return {
        BrowserCredentialsDatabasePath(
            database_file_path=Path(
                f"{tmp_path}/home/{USERNAME_1}/{GOOGLE_CHROME_PATH}/Default/Login Data"
            ),
            master_key=DEFAULT_MASTER_KEY,
        ),
        BrowserCredentialsDatabasePath(
            database_file_path=Path(
                f"{tmp_path}/home/{USERNAME_2}/{GOOGLE_CHROME_PATH}/Default/Login Data"
            ),
            master_key=DEFAULT_MASTER_KEY,
        ),
        BrowserCredentialsDatabasePath(
            database_file_path=Path(f"{tmp_path}/home/{USERNAME_2}/{CHROMIUM_PATH}/Login Data"),
            master_key=DEFAULT_MASTER_KEY,
        ),
    }


def test_linux_credentials_database_selector(
    patch_pwd_getpwall,
    linux_credentials_database_selector,
    expected_login_database_paths,
):
    actual_login_database_paths = linux_credentials_database_selector()

    assert len(actual_login_database_paths) == len(expected_login_database_paths)
    assert actual_login_database_paths == expected_login_database_paths


@pytest.mark.parametrize(
    "method, error",
    [
        ("exists", PermissionError),
        ("exists", OSError),
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

    assert list(actual_login_database_paths) == []


@pytest.mark.parametrize(
    "method, error",
    [
        ("glob", PermissionError),
        ("glob", OSError),
    ],
)
def test_linux_credentials_database_selector__glob_exception(
    monkeypatch, patch_pwd_getpwall, linux_credentials_database_selector, error, method
):
    def mock_method(pattern, al):
        raise error()

    monkeypatch.setattr(
        f"agent_plugins.credentials_collectors.chrome.src.linux_credentials_database_selector.Path.{method}",  # noqa: E501
        mock_method,
    )
    actual_login_database_paths = linux_credentials_database_selector()

    assert list(actual_login_database_paths) == []
