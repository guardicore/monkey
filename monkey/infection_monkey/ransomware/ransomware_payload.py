import logging
from pathlib import Path

from infection_monkey.ransomware.valid_file_extensions import VALID_FILE_EXTENSIONS_FOR_ENCRYPTION
from infection_monkey.utils.dir_utils import (
    file_extension_filter,
    filter_files,
    get_all_regular_files_in_directory,
    is_not_symlink_filter,
)
from infection_monkey.utils.environment import is_windows_os

LOG = logging.getLogger(__name__)


class RansomewarePayload:
    def __init__(self, config: dict):
        LOG.info(f"Windows dir configured for encryption is " f"{config['windows_dir']}")
        LOG.info(f"Linux dir configured for encryption is " f"{config['linux_dir']}")

        self.target_dir = Path(config["windows_dir"] if is_windows_os() else config["linux_dir"])

    def run_payload(self):
        file_list = self._find_files()
        self._encrypt_files(file_list)

    def _find_files(self):
        file_filters = [
            file_extension_filter(VALID_FILE_EXTENSIONS_FOR_ENCRYPTION),
            is_not_symlink_filter,
        ]

        all_files = get_all_regular_files_in_directory(self.target_dir)
        return filter_files(all_files, file_filters)

    def _encrypt_files(self, file_list):
        for file in file_list:
            self._encrypt_file(file)

    def _encrypt_file(self, file):
        pass
