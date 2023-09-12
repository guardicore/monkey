from typing import Collection

from .browser_credentials_database_path import BrowserCredentialsDatabasePath


class LinuxCredentialsDatabaseSelector:
    def __init__(self):
        pass

    def __call__(self) -> Collection[BrowserCredentialsDatabasePath]:
        return []
