from pathlib import Path
from typing import Callable, Iterable, List, Set


def get_all_regular_files_in_directory(dir_path: Path) -> List[Path]:
    return filter_files(dir_path.iterdir(), [lambda f: f.is_file()])


def filter_files(files: Iterable[Path], file_filters: List[Callable[[Path], bool]]):
    filtered_files = files
    for file_filter in file_filters:
        filtered_files = [f for f in filtered_files if file_filter(f)]

    return filtered_files


def file_extension_filter(file_extensions: Set):
    def inner_filter(f: Path):
        return f.suffix in file_extensions

    return inner_filter


def is_not_symlink_filter(f: Path):
    return not f.is_symlink()
