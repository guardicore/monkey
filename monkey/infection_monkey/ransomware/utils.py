import os
from typing import List

from infection_monkey.ransomware.valid_file_extensions import VALID_FILE_EXTENSIONS_FOR_ENCRYPTION


def get_files_to_encrypt(dir_path: str) -> List[str]:
    all_files = get_all_files_in_directory(dir_path)

    files_to_encrypt = []
    for file in all_files:
        if os.path.splitext(file)[1] in VALID_FILE_EXTENSIONS_FOR_ENCRYPTION:
            files_to_encrypt.append(file)

    return files_to_encrypt


def get_all_files_in_directory(dir_path: str) -> List:
    return list(
        filter(os.path.isfile, [os.path.join(dir_path, item) for item in os.listdir(dir_path)])
    )
