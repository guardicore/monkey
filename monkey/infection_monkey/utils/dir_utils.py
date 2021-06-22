from pathlib import Path
from typing import Callable, List


def get_all_files_in_directory(dir_path: Path) -> List[Path]:
    return [f for f in dir_path.iterdir() if f.is_file()]


def filter_files(files: List[Path], file_filter: Callable[[Path], bool]):
    return [f for f in files if file_filter(f)]
