from pathlib import Path
from typing import List, Set

from common.utils.file_utils import get_file_sha256_hash
from infection_monkey.utils.dir_utils import (
    file_extension_filter,
    filter_files,
    get_all_regular_files_in_directory,
    is_not_shortcut_filter,
    is_not_symlink_filter,
)

from .consts import README_FILE_NAME, README_SHA256_HASH


class ProductionSafeTargetFileSelector:
    def __init__(self, targeted_file_extensions: Set[str]):
        self._targeted_file_extensions = targeted_file_extensions

    def __call__(self, target_dir: Path) -> List[Path]:
        file_filters = [
            file_extension_filter(self._targeted_file_extensions),
            is_not_shortcut_filter,
            is_not_symlink_filter,
            _is_not_ransomware_readme_filter,
        ]

        all_files = get_all_regular_files_in_directory(target_dir)
        return filter_files(all_files, file_filters)


def _is_not_ransomware_readme_filter(filepath: Path) -> bool:
    if filepath.name != README_FILE_NAME:
        return True

    return get_file_sha256_hash(filepath) != README_SHA256_HASH
