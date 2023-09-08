import base64
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from agent_plugins.credentials_collectors.chrome.src.utils import BrowserCredentialsDatabasePath

EDGE_DECRYPTED_MASTER_KEY = b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
EDGE_MASTER_KEY = b"DPAPI\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
EDGE_LOCAL_STATE = {
    "profile": {"info_cache": {"Default": {}}},
    "os_crypt": {"encrypted_key": base64.b64encode(EDGE_MASTER_KEY).decode()},
}
CHROME_DECRYPTED_MASTER_KEY = b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
CHROME_MASTER_KEY = b"DPAPI\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
CHROME_LOCAL_STATE = {
    "profile": {"info_cache": {"Default": {}}},
    "os_crypt": {"encrypted_key": base64.b64encode(CHROME_MASTER_KEY).decode()},
}


class MockChromeAppDataDir:
    def __init__(self, path):
        self._path = path

    def add_browser_data_dir(self, data_dir_path):
        data_dir = self._path / data_dir_path
        data_dir.mkdir(parents=True)

        return MockChromeBrowserDataDir(data_dir)


class MockChromeBrowserDataDir:
    def __init__(self, path):
        self._path = path

    def with_local_state(self, local_state):
        with open(self._path / "Local State", "w") as file:
            json.dump(local_state, file)

        return self

    def with_profile(self, profile_name, create_database=True):
        profile_dir = self._path / profile_name
        profile_dir.mkdir()

        if create_database:
            Path(profile_dir / "Login Data").touch()

        return self


@pytest.fixture
def mock_appdata_dir(setup_appdata_dir):
    def build_appdata_dir(appdata_dir_builder):
        (
            appdata_dir_builder.add_browser_data_dir("Microsoft/Edge/User Data")
            .with_local_state(EDGE_LOCAL_STATE)
            .with_profile("Default")
        )
        (
            appdata_dir_builder.add_browser_data_dir("Google/Chrome/User Data")
            .with_local_state(CHROME_LOCAL_STATE)
            .with_profile("Default")
        )

    return setup_appdata_dir(build_appdata_dir)


@pytest.fixture
def mock_appdata_dir_with_no_master_key(setup_appdata_dir):
    edge_local_state_no_master_key = EDGE_LOCAL_STATE.copy()
    edge_local_state_no_master_key["os_crypt"]["encrypted_key"] = None
    chrome_local_state_no_master_key = CHROME_LOCAL_STATE.copy()
    chrome_local_state_no_master_key["os_crypt"]["encrypted_key"] = None

    def build_appdata_dir(appdata_dir_builder):
        (
            appdata_dir_builder.add_browser_data_dir("Microsoft/Edge/User Data")
            .with_local_state(edge_local_state_no_master_key)
            .with_profile("Default")
        )
        (
            appdata_dir_builder.add_browser_data_dir("Google/Chrome/User Data")
            .with_local_state(chrome_local_state_no_master_key)
            .with_profile("Default")
        )

    return setup_appdata_dir(build_appdata_dir)


@pytest.fixture
def mock_appdata_dir_with_no_databases(setup_appdata_dir):
    def build_appdata_dir(appdata_dir_builder):
        (
            appdata_dir_builder.add_browser_data_dir("Microsoft/Edge/User Data")
            .with_local_state(EDGE_LOCAL_STATE)
            .with_profile("Default", create_database=False)
        )
        (
            appdata_dir_builder.add_browser_data_dir("Google/Chrome/User Data")
            .with_local_state(CHROME_LOCAL_STATE)
            .with_profile("Default", create_database=False)
        )

    return setup_appdata_dir(build_appdata_dir)


@pytest.fixture
def mock_appdata_dir_with_no_profile_dirs(setup_appdata_dir):
    def build_appdata_dir(appdata_dir_builder):
        appdata_dir_builder.add_browser_data_dir("Microsoft/Edge/User Data").with_local_state(
            EDGE_LOCAL_STATE
        )
        appdata_dir_builder.add_browser_data_dir("Google/Chrome/User Data").with_local_state(
            CHROME_LOCAL_STATE
        )

    return setup_appdata_dir(build_appdata_dir)


@pytest.fixture
def setup_appdata_dir(monkeypatch, tmp_path):
    def inner(build_appdata_dir):
        appdata_dir = tmp_path / "appdata"
        appdata_dir.mkdir()

        appdata_dir_builder = MockChromeAppDataDir(appdata_dir)
        build_appdata_dir(appdata_dir_builder)

        monkeypatch.setenv("LOCALAPPDATA", str(appdata_dir))

        return appdata_dir

    return inner


@pytest.fixture(scope="module", autouse=True)
def patch_windows_utils():
    def mock_win32crypt_unprotect_data(master_key):
        return master_key

    windows_utils = MagicMock()
    windows_utils.win32crypt_unprotect_data = mock_win32crypt_unprotect_data
    sys.modules["agent_plugins.credentials_collectors.chrome.src.windows_utils"] = windows_utils


@pytest.fixture
def database_selector():
    from agent_plugins.credentials_collectors.chrome.src.windows_credentials_database_selector import (  # noqa: E501
        WindowsCredentialsDatabaseSelector,
    )

    return WindowsCredentialsDatabaseSelector()


def test__finds_databases(mock_appdata_dir, database_selector):
    databases = database_selector()

    expected_edge_database = BrowserCredentialsDatabasePath(
        mock_appdata_dir / "Microsoft" / "Edge" / "User Data" / "Default" / "Login Data",
        EDGE_DECRYPTED_MASTER_KEY,
    )
    expected_chrome_database = BrowserCredentialsDatabasePath(
        mock_appdata_dir / "Google" / "Chrome" / "User Data" / "Default" / "Login Data",
        CHROME_DECRYPTED_MASTER_KEY,
    )
    assert len(databases) == 2
    assert expected_edge_database in databases
    assert expected_chrome_database in databases


def test__outputs_none_if_no_master_key(mock_appdata_dir_with_no_master_key, database_selector):
    databases = database_selector()

    expected_edge_database = BrowserCredentialsDatabasePath(
        mock_appdata_dir_with_no_master_key
        / "Microsoft"
        / "Edge"
        / "User Data"
        / "Default"
        / "Login Data",
        None,
    )
    expected_chrome_database = BrowserCredentialsDatabasePath(
        mock_appdata_dir_with_no_master_key
        / "Google"
        / "Chrome"
        / "User Data"
        / "Default"
        / "Login Data",
        None,
    )
    assert len(databases) == 2
    assert expected_edge_database in databases
    assert expected_chrome_database in databases


@pytest.mark.usefixtures("mock_appdata_dir_with_no_databases")
def test__outputs_empty_collection_if_no_databases(database_selector):
    databases = database_selector()

    assert len(databases) == 0


@pytest.mark.usefixtures("mock_appdata_dir_with_no_profile_dirs")
def test__outputs_empty_collection_if_no_profiles(database_selector):
    databases = database_selector()

    assert len(databases) == 0
