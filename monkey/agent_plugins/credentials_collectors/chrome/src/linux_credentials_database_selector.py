from typing import Collection

from .utils import BrowserCredentialsDatabasePath


class LinuxCredentialsDatabaseSelector:
    def __init__(self):
        pass

    def __call__(self) -> Collection[BrowserCredentialsDatabasePath]:
        return []
