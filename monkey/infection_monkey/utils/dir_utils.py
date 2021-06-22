from pathlib import Path
from typing import List


def get_all_files_in_directory(dir_path: str) -> List:
    path = Path(dir_path)

    return [str(f) for f in path.iterdir() if f.is_file()]
