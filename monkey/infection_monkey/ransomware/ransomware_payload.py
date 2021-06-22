import logging

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
        return []

    def _encrypt_files(self, file_list):
        for file in file_list:
            self._encrypt_file(file)

    def _encrypt_file(self, file):
        pass
