import logging
import os

from monkey_island.cc.server_utils.file_utils import create_secure_directory

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
        custom_pba_dir = cls.get_custom_pba_directory()
        create_secure_directory(custom_pba_dir)

    @staticmethod
    def save_file(filename: str, file_contents: bytes):
        file_path = os.path.join(PostBreachFilesService.get_custom_pba_directory(), filename)
        with open(file_path, "wb") as f:
            f.write(file_contents)

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
