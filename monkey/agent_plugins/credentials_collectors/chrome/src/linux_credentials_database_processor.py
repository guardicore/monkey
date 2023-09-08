from typing import Collection

from common.credentials import Credentials
from common.types import Event

from .utils import BrowserCredentialsDatabasePath


class LinuxCredentialsDatabaseProcessor:
    def __init__(self):
        pass

    def __call__(
        self, interrupt: Event, database_paths: Collection[BrowserCredentialsDatabasePath]
    ) -> Collection[Credentials]:
        return []
