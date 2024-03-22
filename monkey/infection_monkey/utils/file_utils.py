import ctypes
import logging
from pathlib import WindowsPath

logger = logging.getLogger(__name__)

MOVEFILE_DELAY_UNTIL_REBOOT = 4


def mark_file_for_deletion_on_windows(file_path: WindowsPath):
    file_source_path_ctypes = ctypes.c_char_p(str(file_path).encode())

    mark_file_response = ctypes.windll.kernel32.MoveFileExA(  # type: ignore [attr-defined]
        file_source_path_ctypes, None, MOVEFILE_DELAY_UNTIL_REBOOT
    )

    if mark_file_response == 0:
        error_message = ctypes.FormatError(  # type: ignore [attr-defined]
            ctypes.windll.kernel32.GetLastError()  # type: ignore [attr-defined]
        )
        logger.debug(f"Error marking file {file_path} for deletion on next boot: {error_message}")
        return

    logger.debug(f"File {file_path} is marked for deletion on next boot")
