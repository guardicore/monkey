from pathlib import Path
from typing import List, Set

from infection_monkey.utils.dir_utils import (
    file_extension_filter,
    filter_files,
    get_all_regular_files_in_directory,
    is_not_shortcut_filter,
    is_not_symlink_filter,
)


def select_production_safe_target_files(target_dir: Path, extensions: Set) -> List[Path]:
    file_filters = [
        file_extension_filter(extensions),
        is_not_shortcut_filter,
        is_not_symlink_filter,
    ]

    all_files = get_all_regular_files_in_directory(target_dir)
    return filter_files(all_files, file_filters)
