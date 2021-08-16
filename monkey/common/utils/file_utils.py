import hashlib
import os
from pathlib import Path


class InvalidPath(Exception):
    pass


def expand_path(path: str) -> Path:
    if not path:
        raise InvalidPath("Empty path provided")

    return Path(os.path.expandvars(os.path.expanduser(path)))


def get_file_sha256_hash(filepath: Path):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            sha256.update(block)

    return sha256.hexdigest()
