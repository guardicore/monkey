import logging
import os
import pwd
from pathlib import Path, PurePath
from typing import Dict, Sequence, Collection

from .browser_credentials_database_path import BrowserCredentialsDatabasePath

logger = logging.getLogger(__name__)

LinuxUsername = str
UserDirectories = Dict[LinuxUsername, PurePath]


CHROMIUM_BASED_DB_PATHS = [
    ("Google Chrome", ".config/google-chrome"),
    ("Chromium", ".config/chromium"),
    ("Brave", ".config/BraveSoftware/Brave-Browser"),
    ("SlimJet", ".config/slimjet"),
    ("Dissenter Browser", ".config/GabAI/Dissenter-Browser"),
    ("Vivaldi", ".config/vivaldi"),
    ("Microsoft Edge (Dev)", ".config/microsoft-edge-dev"),
    ("Microsoft Edge (Beta)", ".config/microsoft-edge-beta"),
    ("Microsoft Edge", ".config/microsoft-edge"),
]


class LinuxCredentialsDatabaseSelector:
    def __call__(self) -> Collection[BrowserCredentialsDatabasePath]:
        login_database_paths = []
        for profile_dir in self._get_browser_database_paths():
            try:
                sub_profile_dirs = os.listdir(profile_dir)
            except Exception:
                logger.debug(f"Could not list {profile_dir}")
                continue

            for subdir in sub_profile_dirs:
                login_database_path = profile_dir / subdir / "Login Data"
                if Path(login_database_path).is_file():
                    login_database_paths.append(login_database_path)

        return login_database_paths

    def _get_browser_database_paths(self) -> Sequence[PurePath]:
        database_paths = []

        for username, home_dir_path in self._get_home_directories().items():
            for browser_name, browser_path in CHROMIUM_BASED_DB_PATHS:
                browser_db_path = home_dir_path / browser_path
                try:
                    if self._is_valid_dir(browser_db_path):
                        database_paths.append(browser_db_path)
                except Exception as err:
                    logger.exception(
                        f"Failed to get {browser_name} database path for {username}: {err}"
                    )

        return database_paths

    def _is_valid_dir(self, path: PurePath) -> bool:
        try:
            return Path(path).is_dir()
        except PermissionError as err:
            logger.debug(f"Failed to validate path {path}: {err}")
            return False

    def _get_home_directories(self) -> UserDirectories:
        """
        Retrieve all users' home directories
        """
        try:
            home_dirs = {
                p.pw_name: PurePath(p.pw_dir) for p in pwd.getpwall()  # type: ignore[attr-defined]
            }
            if "HOME" in os.environ:
                home_path = PurePath(os.environ["HOME"])
                if home_path not in home_dirs.values():
                    home_dirs[os.getlogin()] = home_path

            return home_dirs
        except Exception:
            logger.exception("Failed to get user directories")
            return {}
>>>>>>> a0b744f07 (Chrome: Implement LinuxCredentialsDatabaseSelector)
