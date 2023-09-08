import getpass
import logging
from pathlib import PureWindowsPath
from typing import Collection, Dict, Optional, Set, Tuple

from .chrome_browser_local_data import ChromeBrowserLocalData
from .windows_utils import win32crypt_unprotect_data

logger = logging.getLogger(__name__)

DRIVE = "C"
LOCAL_APPDATA = "{drive}:\\Users\\{user}\\AppData\\Local"

WINDOWS_BROWSERS = {
    "Chromium Edge": "{local_appdata}\\Microsoft\\Edge\\User Data",
    "Google Chrome": "{local_appdata}\\Google\\Chrome\\User Data",
}


class WindowsChromeBrowserLocalData(ChromeBrowserLocalData):
    def get_master_key(self) -> Optional[bytes]:
        try:
            master_key = super().get_master_key()
            master_key = master_key[5:]  # removing DPAPI
            master_key = win32crypt_unprotect_data(
                master_key,
            )
            return master_key
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

        self._browsers: Dict[str, PureWindowsPath] = {}
        for browser_name, browser_directory in WINDOWS_BROWSERS.items():
            self._browsers[browser_name] = PureWindowsPath(
                browser_directory.format(local_appdata=local_appdata)
            )

    def __call__(self) -> Set[Tuple[PureWindowsPath, Optional[bytes]]]:
        """
        Get browsers' credentials' database directories for current user
        """

        databases: Set[Tuple[PureWindowsPath, Optional[bytes]]] = set()

        for browser_name, browser_local_data_directory_path in self._browsers.items():
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

            databases = databases.union(browser_databases)

        return databases

    @staticmethod
    def _get_credentials_database_paths_for_browser(
        browser_local_data_directory_path: PureWindowsPath,
    ) -> Collection[Tuple[PureWindowsPath, Optional[bytes]]]:
        paths: Set[Tuple[PureWindowsPath, Optional[bytes]]] = set()

        try:
            local_data = WindowsChromeBrowserLocalData(browser_local_data_directory_path)
        except Exception:
            return paths

        master_key = local_data.get_master_key()
        paths_for_each_profile = local_data.get_credentials_database_paths()
        paths = paths.union((path, master_key) for path in paths_for_each_profile)

        return paths
