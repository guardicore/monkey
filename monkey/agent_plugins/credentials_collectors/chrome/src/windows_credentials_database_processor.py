from typing import Collection

from common.credentials import Credentials
from common.types import Event

from .browser_credentials_database_path import BrowserCredentialsDatabasePath


class WindowsCredentialsDatabaseProcessor:
    def __init__(self):
        pass

    def __call__(
        self, interrupt: Event, database_paths: Collection[BrowserCredentialsDatabasePath]
    ) -> Collection[Credentials]:
        return []
