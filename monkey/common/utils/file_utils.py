import os
from pathlib import Path


class InvalidPath(Exception):
    pass


def expand_path(path: str) -> Path:
    if not path:
        raise InvalidPath("Empty path provided")

    return Path(os.path.expandvars(os.path.expanduser(path)))
