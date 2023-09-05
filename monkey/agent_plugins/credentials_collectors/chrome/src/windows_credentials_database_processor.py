from pathlib import PureWindowsPath
from typing import Sequence

from common.credentials import Credentials


class WindowsCredentialsDatabaseProcessor:
    def __init__(self):
        pass

    def __call__(self, database_paths: Sequence[PureWindowsPath]) -> Sequence[Credentials]:
        return []
