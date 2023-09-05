from pathlib import PurePath
from typing import Sequence


class LinuxCredentialsDatabaseSelector:
    def __init__(self):
        pass

    def __call__(self) -> Sequence[PurePath]:
        return []
