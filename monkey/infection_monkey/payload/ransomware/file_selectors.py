import filecmp
import logging
from itertools import chain
from pathlib import Path
from typing import Iterable, Set

from common.utils.file_utils import (
    get_all_regular_files_in_directory,
    get_all_subdirectories_of_directory,
)
from infection_monkey.utils.file_utils import (
    file_extension_filter,
    filter_files,
    is_not_shortcut_filter,
    is_not_symlink_filter,
)

from .consts import README_FILE_NAME, README_SRC

logger = logging.getLogger(__name__)


class ProductionSafeTargetFileSelector:
    def __init__(self, targeted_file_extensions: Set[str]):
        self._targeted_file_extensions = targeted_file_extensions

    def __call__(self, target_dir: Path) -> Iterable[Path]:
        if not target_dir.exists():
            logger.warning(f"Target directory {target_dir} does not exist")
            return iter([])

        if not target_dir.is_dir():
            logger.warning(f"Target directory {target_dir} is not a directory")
            return iter([])

        if target_dir.is_symlink():
            logger.warning(
                "The ProductionSafeTargetFileSelector will not follow symlinks - skipping "
                f"{target_dir}"
            )
            return iter([])

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

    return not filecmp.cmp(filepath, README_SRC)


class RecursiveTargetFileSelector:
    def __init__(self, targeted_file_extensions: Set[str]):
        self._production_safe_target_file_selector = ProductionSafeTargetFileSelector(
            targeted_file_extensions
        )

    def __call__(self, target_dir: Path) -> Iterable[Path]:
        if not target_dir.exists():
            logger.warning(f"Target directory {target_dir} does not exist")
            return iter([])

        if not target_dir.is_dir():
            logger.warning(f"Target directory {target_dir} is not a directory")
            return iter([])

        if target_dir.is_symlink():
            logger.warning(
                "The ProductionSafeTargetFileSelector will not follow symlinks - skipping "
                f"{target_dir}"
            )
            return iter([])

        all_subdirectories = get_all_subdirectories_of_directory(target_dir)
        return chain(
            self._production_safe_target_file_selector(target_dir),
            chain.from_iterable(map(self, all_subdirectories)),
        )
