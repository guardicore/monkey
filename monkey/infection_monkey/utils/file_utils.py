import os
from typing import List


def get_all_files_in_directory(dir_path: str) -> List:
    return list(
        filter(os.path.isfile, [os.path.join(dir_path, item) for item in os.listdir(dir_path)])
    )
