from pathlib import PureWindowsPath
from typing import Sequence


class WindowsCredentialsDatabaseSelector:
    def __init__(self):
        pass

    def __call__(self) -> Sequence[PureWindowsPath]:
        return []
