import logging

from infection_monkey.ransomware.utils import get_files_to_encrypt
from infection_monkey.utils.environment import is_windows_os

LOG = logging.getLogger(__name__)


class RansomewarePayload:
    def __init__(self, config: dict):
        self.config = config

    def run_payload(self):
        LOG.info(
            f"Windows dir configured for encryption is " f"{self.config['windows_dir_ransom']}"
        )
        LOG.info(f"Linux dir configured for encryption is " f"{self.config['linux_dir_ransom']}")

        file_list = self._find_files()
        self._encrypt_files(file_list)

    def _find_files(self):
        dir_path = (
            self.config["windows_dir_ransom"]
            if is_windows_os()
            else self.config["linux_dir_ransom"]
        )
        return get_files_to_encrypt(dir_path)

    def _encrypt_files(self, file_list):
        for file in file_list:
            self._encrypt_file(file)

    def _encrypt_file(self, file):
        pass
