import ctypes
import os
from pathlib import Path
from typing import Iterable


def is_user_admin():
    if os.name == "posix":
        return os.getuid() == 0

    return ctypes.windll.shell32.IsUserAnAdmin()


def raise_(ex):
    raise ex


def add_subdirs_to_dir(parent_dir: Path, subdirs: Iterable[str]) -> Iterable[Path]:
    subdir_paths = [parent_dir / s for s in subdirs]

    for subdir in subdir_paths:
        subdir.mkdir()

    return subdir_paths


def add_files_to_dir(parent_dir: Path, file_names: Iterable[str]) -> Iterable[Path]:
    files = [parent_dir / f for f in file_names]

    for f in files:
        f.touch()

    return files
