import ctypes
import hashlib
import os
from pathlib import Path


def is_user_admin():
    if os.name == "posix":
        return os.getuid() == 0

    return ctypes.windll.shell32.IsUserAnAdmin()


def hash_file(filepath: Path):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            sha256.update(block)

    return sha256.hexdigest()


def raise_(ex):
    raise ex
