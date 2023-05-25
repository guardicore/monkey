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


class InvalidTargetError(Exception):
    """Raised when the specified target directory cannot be used as a target."""


def _validate_target_directory(target_dir: Path):
    if not target_dir.exists():
        logger.warning(f"Target directory {target_dir} does not exist")
        raise InvalidTargetError()

    if not target_dir.is_dir():
        logger.warning(f"Target directory {target_dir} is not a directory")
        raise InvalidTargetError()

    if target_dir.is_symlink():
        logger.warning("Following symlinks is not safe in production - skipping " f"{target_dir}")
        raise InvalidTargetError()


class ProductionSafeTargetFileSelector:
    def __init__(self, targeted_file_extensions: Set[str]):
        self._targeted_file_extensions = targeted_file_extensions

    def __call__(self, target_dir: Path) -> Iterable[Path]:
        try:
            _validate_target_directory(target_dir)
        except InvalidTargetError:
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
        try:
            _validate_target_directory(target_dir)
        except InvalidTargetError:
            return iter([])

        all_subdirectories = get_all_subdirectories_of_directory(target_dir)
        return chain(
            self._production_safe_target_file_selector(target_dir),
            chain.from_iterable(map(self, all_subdirectories)),
        )
