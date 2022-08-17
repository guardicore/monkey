import logging

from common.utils.file_utils import InvalidPath, expand_path
from infection_monkey.utils.environment import is_windows_os

logger = logging.getLogger(__name__)


class RansomwareOptions:
    def __init__(self, options: dict):
        self.encryption_enabled = options["encryption"]["enabled"]
        self.file_extension = options["encryption"]["file_extension"]
        self.readme_enabled = options["other_behaviors"]["readme"]

        self.target_directory = None
        self._set_target_directory(options["encryption"]["directories"])

    def _set_target_directory(self, os_target_directories: dict):
        if is_windows_os():
            target_directory = os_target_directories["windows_target_dir"]
        else:
            target_directory = os_target_directories["linux_target_dir"]

        try:
            self.target_directory = expand_path(target_directory)
        except InvalidPath as e:
            logger.debug(f"Target ransomware directory set to None: {e}")
            self.target_directory = None
