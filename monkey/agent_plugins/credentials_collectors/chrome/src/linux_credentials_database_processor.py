from pathlib import PurePosixPath
from typing import Sequence

from common.credentials import Credentials


class LinuxCredentialsDatabaseProcessor:
    def __init__(self):
        pass

    def __call__(self, database_paths: Sequence[PurePosixPath]) -> Sequence[Credentials]:
        return []
