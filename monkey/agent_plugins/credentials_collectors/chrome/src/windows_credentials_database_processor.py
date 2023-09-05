from pathlib import PurePath
from typing import Sequence

from common.credentials import Credentials


class WindowsCredentialsDatabaseProcessor:
    def __init__(self):
        pass

    def __call__(self, database_paths: Sequence[PurePath]) -> Sequence[Credentials]:
        return []
