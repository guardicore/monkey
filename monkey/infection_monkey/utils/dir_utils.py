from pathlib import Path
from typing import List


def get_all_files_in_directory(dir_path: Path) -> List[Path]:
    return [f for f in dir_path.iterdir() if f.is_file()]
