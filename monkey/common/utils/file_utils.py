import hashlib
import os
from pathlib import Path
from typing import BinaryIO, Iterable

MAX_BLOCK_SIZE = 65536


class InvalidPath(Exception):
    pass


def expand_path(path: str) -> Path:
    if not path:
        raise InvalidPath("Empty path provided")

    return Path(os.path.expandvars(os.path.expanduser(path)))


def get_file_sha256_hash(filepath: Path) -> str:
    """
    Calculates sha256 hash from a file path

    :param filepath: A Path object which defines file on the system
    :return sha256 hash of the file
    """
    with open(filepath, "rb") as f:
        return get_binary_io_sha256_hash(f)


def get_binary_io_sha256_hash(binary: BinaryIO) -> str:
    """
    Calculates sha256 hash from a file-like object

    :param binary: file-like object from which we calculate the hash
    :return: sha256 hash from the file-like object
    """
    sha256 = hashlib.sha256()
    for block in iter(lambda: binary.read(MAX_BLOCK_SIZE), b""):
        sha256.update(block)

    return sha256.hexdigest()


def get_all_regular_files_in_directory(dir_path: Path) -> Iterable[Path]:
    return filter(lambda f: f.is_file(), dir_path.iterdir())
