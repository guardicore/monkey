import logging
import os
import pwd
from pathlib import Path
from typing import Collection, Dict, Sequence, Set

from .browser_credentials_database_path import BrowserCredentialsDatabasePath

logger = logging.getLogger(__name__)

LinuxUsername = str
UserDirectories = Dict[LinuxUsername, Path]

# If we don't use a password manager to store an auto-fill password
# then Linux uses a default master key to "encrypt" the passwords
# which funny enough it is 'peanuts'
DEFAULT_MASTER_KEY = "peanuts".encode()

LOGIN_DATABASE_FILENAME = "Login Data"
CHROMIUM_BASED_DB_PATHS = [
    ("Google Chrome", ".config/google-chrome"),
    ("Chromium", ".config/chromium"),
]


class LinuxCredentialsDatabaseSelector:
    def __call__(self) -> Collection[BrowserCredentialsDatabasePath]:
        database_paths: Set[BrowserCredentialsDatabasePath] = set()
        for profile_dir in self._get_browser_database_paths():
            login_data_paths = self._get_login_data_paths(profile_dir)
            database_paths.update(login_data_paths)

        return database_paths

    def _get_login_data_paths(
        self, profile_dir_path: Path
    ) -> Collection[BrowserCredentialsDatabasePath]:
        login_data_paths: Set[BrowserCredentialsDatabasePath] = set()
        try:
            sub_profile_dirs = profile_dir_path.iterdir()
            for subdir in sub_profile_dirs:
                if subdir == (profile_dir_path / LOGIN_DATABASE_FILENAME):
                    if self._file_is_accessible(subdir):
                        login_data_paths.add(
                            BrowserCredentialsDatabasePath(
                                database_file_path=subdir, master_key=DEFAULT_MASTER_KEY
                            )
                        )

                login_database_path = profile_dir_path / subdir / LOGIN_DATABASE_FILENAME
                if self._file_is_accessible(login_database_path):
                    login_data_paths.add(
                        BrowserCredentialsDatabasePath(
                            database_file_path=login_database_path, master_key=DEFAULT_MASTER_KEY
                        )
                    )
        except Exception as err:
            logger.debug(f"Could not list {profile_dir_path}: {err}")

        return login_data_paths

    @staticmethod
    def _file_is_accessible(path: Path) -> bool:
        try:
            print(path)
            return path.is_file() and os.access(path, os.R_OK)
        except PermissionError as err:
            logger.debug(f"Failed to validate file {path}: {err}")
            return False

    def _get_browser_database_paths(self) -> Sequence[Path]:
        database_paths = []

        for username, home_dir_path in self._get_home_directories().items():
            for browser_name, browser_path in CHROMIUM_BASED_DB_PATHS:
                browser_db_path = home_dir_path / browser_path
                try:
                    if self._directory_is_accessible(browser_db_path):
                        database_paths.append(browser_db_path)
                except Exception as err:
                    logger.exception(
                        f"Failed to get {browser_name} database path for {username}: {err}"
                    )

        return database_paths

    @staticmethod
    def _directory_is_accessible(path: Path) -> bool:
        try:
            return path.is_dir() and os.access(path, os.R_OK)
        except PermissionError as err:
            logger.debug(f"Failed to validate path {path}: {err}")
            return False

    @staticmethod
    def _get_home_directories() -> UserDirectories:
        """
        Retrieve all users' home directories
        """
        try:
            home_dirs = {
                p.pw_name: Path(p.pw_dir) for p in pwd.getpwall()  # type: ignore[attr-defined]
            }
            if "HOME" in os.environ:
                home_path = Path(os.environ["HOME"])
                if home_path not in home_dirs.values():
                    home_dirs[os.getlogin()] = home_path

            return home_dirs
        except Exception:
            logger.exception("Failed to get user directories")
            return {}
