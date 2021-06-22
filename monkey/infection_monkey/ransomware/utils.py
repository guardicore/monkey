from pathlib import Path
from typing import List

from infection_monkey.ransomware.valid_file_extensions import VALID_FILE_EXTENSIONS_FOR_ENCRYPTION
from infection_monkey.utils.dir_utils import (
    file_extension_filter,
    filter_files,
    get_all_files_in_directory,
)


def get_files_to_encrypt(dir_path: str) -> List[Path]:
    all_files = get_all_files_in_directory(Path(dir_path))
    return filter_files(all_files, file_extension_filter(VALID_FILE_EXTENSIONS_FOR_ENCRYPTION))
