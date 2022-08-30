import ctypes
import os
from pathlib import Path
from typing import Iterable, Mapping


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


# This is only needed since values are compared in configuration objects in the tests.
# In practice, the list/tuple differences shouldn't make any difference since both are iterable.
def convert_all_lists_to_tuples_in_mapping(configuration: Mapping):
    for key in configuration:
        value = configuration[key]
        if isinstance(value, list):
            configuration[key] = tuple(value)
        if isinstance(value, Mapping):
            convert_all_lists_to_tuples_in_mapping(value)
    return configuration
