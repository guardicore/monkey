import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class PostBreachFilesService:
    DATA_DIR = None
    CUSTOM_PBA_DIRNAME = "custom_pbas"

    # TODO: A number of these services should be instance objects instead of
    # static/singleton hybrids. At the moment, this requires invasive refactoring that's
    # not a priority.
    @classmethod
    def initialize(cls, data_dir):
        cls.DATA_DIR = data_dir
        Path(cls.get_custom_pba_directory()).mkdir(mode=0o0700, parents=True, exist_ok=True)

    @staticmethod
    def remove_PBA_files():
        for f in os.listdir(PostBreachFilesService.get_custom_pba_directory()):
            PostBreachFilesService.remove_file(f)

    @staticmethod
    def remove_file(file_name):
        file_path = os.path.join(PostBreachFilesService.get_custom_pba_directory(), file_name)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError as e:
            logger.error("Can't remove previously uploaded post breach files: %s" % e)

    @staticmethod
    def get_custom_pba_directory():
        return os.path.join(
            PostBreachFilesService.DATA_DIR, PostBreachFilesService.CUSTOM_PBA_DIRNAME
        )
