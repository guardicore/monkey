import logging
import os
from pathlib import Path

# TODO: Remove circular dependency between ConfigService and PostBreachFilesService.
import monkey_island.cc.services.config

__author__ = "VakarisZ"

logger = logging.getLogger(__name__)

# Where to find file names in config
PBA_WINDOWS_FILENAME_PATH = ["monkey", "post_breach", "PBA_windows_filename"]
PBA_LINUX_FILENAME_PATH = ["monkey", "post_breach", "PBA_linux_filename"]


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
        if monkey_island.cc.services.config.ConfigService.get_config():
            windows_filename = monkey_island.cc.services.config.ConfigService.get_config_value(
                PBA_WINDOWS_FILENAME_PATH
            )
            linux_filename = monkey_island.cc.services.config.ConfigService.get_config_value(
                PBA_LINUX_FILENAME_PATH
            )
            if linux_filename:
                PostBreachFilesService._remove_file(linux_filename)
            if windows_filename:
                PostBreachFilesService._remove_file(windows_filename)

    @staticmethod
    def _remove_file(file_name):
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

    @staticmethod
    def set_config_PBA_files(config_json):
        """
        Sets PBA file info in config_json to current config's PBA file info values.
        :param config_json: config_json that will be modified
        """
        if monkey_island.cc.services.config.ConfigService.get_config():
            linux_filename = monkey_island.cc.services.config.ConfigService.get_config_value(
                PBA_LINUX_FILENAME_PATH
            )
            windows_filename = monkey_island.cc.services.config.ConfigService.get_config_value(
                PBA_WINDOWS_FILENAME_PATH
            )
            config_json["monkey"]["post_breach"]["PBA_linux_filename"] = linux_filename
            config_json["monkey"]["post_breach"]["PBA_windows_filename"] = windows_filename
