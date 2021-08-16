import logging

from common.utils.file_utils import InvalidPath, expand_path
from infection_monkey.utils.environment import is_windows_os

LOG = logging.getLogger(__name__)


class RansomwareConfig:
    def __init__(self, config: dict):
        self.encryption_enabled = config["encryption"]["enabled"]
        self.readme_enabled = config["other_behaviors"]["readme"]

        self.target_directory = None
        self._set_target_directory(config["encryption"]["directories"])

    def _set_target_directory(self, os_target_directories: dict):
        if is_windows_os():
            target_directory = os_target_directories["windows_target_dir"]
        else:
            target_directory = os_target_directories["linux_target_dir"]

        try:
            self.target_directory = expand_path(target_directory)
        except InvalidPath as e:
            LOG.debug(f"Target ransomware directory set to None: {e}")
            self.target_directory = None
