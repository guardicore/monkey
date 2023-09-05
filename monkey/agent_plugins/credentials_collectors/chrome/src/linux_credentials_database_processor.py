from pathlib import PurePath
from typing import Sequence

from common.credentials import Credentials
from common.types import Event


class LinuxCredentialsDatabaseProcessor:
    def __init__(self):
        pass

    def __call__(
        self, interrupt: Event, database_paths: Sequence[PurePath]
    ) -> Sequence[Credentials]:
        return []
