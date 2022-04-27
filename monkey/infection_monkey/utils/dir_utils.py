from pathlib import Path
from typing import Callable, Iterable, Set


def filter_files(
    files: Iterable[Path], file_filters: Iterable[Callable[[Path], bool]]
) -> Iterable[Path]:
    filtered_files = files
    for file_filter in file_filters:
        filtered_files = filter(file_filter, filtered_files)

    return filtered_files


def file_extension_filter(file_extensions: Set) -> Callable[[Path], bool]:
    def inner_filter(f: Path) -> bool:
        return f.suffix in file_extensions

    return inner_filter


def is_not_symlink_filter(f: Path) -> bool:
    return not f.is_symlink()


def is_not_shortcut_filter(f: Path) -> bool:
    return f.suffix != ".lnk"
