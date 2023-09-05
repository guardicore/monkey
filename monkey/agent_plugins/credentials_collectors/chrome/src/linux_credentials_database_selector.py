from pathlib import PurePosixPath
from typing import Sequence


class LinuxCredentialsDatabaseSelector:
    def __init__(self):
        pass

    def __call__(self) -> Sequence[PurePosixPath]:
        return []
