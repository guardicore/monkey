import ctypes
import logging
from pathlib import Path, WindowsPath
from typing import Callable, Iterable, Set

from common.utils.code_utils import apply_filters

logger = logging.getLogger(__name__)

MOVEFILE_DELAY_UNTIL_REBOOT = 4


def filter_files(
    files: Iterable[Path], file_filters: Iterable[Callable[[Path], bool]]
) -> Iterable[Path]:
    return apply_filters(files, file_filters)


def file_extension_filter(file_extensions: Set) -> Callable[[Path], bool]:
    def inner_filter(f: Path) -> bool:
        return f.suffix in file_extensions

    return inner_filter


def is_not_symlink_filter(f: Path) -> bool:
    return not f.is_symlink()


def is_not_shortcut_filter(f: Path) -> bool:
    return f.suffix != ".lnk"


def mark_file_for_deletion_on_windows(file_path: WindowsPath):
    file_source_path_ctypes = ctypes.c_char_p(str(file_path).encode())

    mark_file_response = ctypes.windll.kernel32.MoveFileExA(
        file_source_path_ctypes, None, MOVEFILE_DELAY_UNTIL_REBOOT
    )

    if mark_file_response == 0:
        logger.debug(
            f"Error marking file {file_path} for deletion on next boot:"
            f"{ctypes.windll.kernel32.GetLastError()}"
        )
        return

    logger.debug(f"File {file_path} is marked for deletion on next boot")
