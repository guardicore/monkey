import logging
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
        for browser_database_path in self._get_browser_database_paths():
            login_data_paths = self._get_login_data_paths(browser_database_path)
            database_paths.update(login_data_paths)

        return database_paths

    def _get_browser_database_paths(self) -> Sequence[Path]:
        database_paths = []

        for username, home_dir_path in self._get_home_directories().items():
            for browser_name, browser_path in CHROMIUM_BASED_DB_PATHS:
                browser_db_path = home_dir_path / browser_path
                try:
                    if browser_db_path.exists():
                        database_paths.append(browser_db_path)
                except Exception as err:
                    logger.exception(
                        f"Failed to get {browser_name} database path for {username}: {err}"
                    )

        return database_paths

    @staticmethod
    def _get_home_directories() -> UserDirectories:
        """
        Retrieve all users' home directories
        """
        try:
            home_dirs = {
                p.pw_name: Path(p.pw_dir) for p in pwd.getpwall()  # type: ignore[attr-defined]
            }

            return home_dirs
        except Exception:
            logger.exception("Failed to get user directories")
            return {}

    def _get_login_data_paths(
        self, browser_database_path: Path
    ) -> Collection[BrowserCredentialsDatabasePath]:
        login_data_paths: Set[BrowserCredentialsDatabasePath] = set()
        try:
            if (browser_database_path / LOGIN_DATABASE_FILENAME).exists():
                login_data_paths.add(
                    BrowserCredentialsDatabasePath(
                        database_file_path=(browser_database_path / LOGIN_DATABASE_FILENAME),
                        master_key=DEFAULT_MASTER_KEY,
                    )
                )

            sub_browser_database_paths = browser_database_path.iterdir()
            for subdir in sub_browser_database_paths:
                login_database_path = browser_database_path / subdir / LOGIN_DATABASE_FILENAME
                if login_database_path.exists():
                    login_data_paths.add(
                        BrowserCredentialsDatabasePath(
                            database_file_path=login_database_path, master_key=DEFAULT_MASTER_KEY
                        )
                    )
        except Exception as err:
            logger.debug(f"Could not list {browser_database_path}: {err}")

        return login_data_paths
