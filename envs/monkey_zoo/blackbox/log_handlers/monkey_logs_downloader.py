import logging

from envs.monkey_zoo.blackbox.log_handlers.monkey_log import MonkeyLog

LOGGER = logging.getLogger(__name__)


class MonkeyLogsDownloader(object):

    def __init__(self, island_client, log_dir_path):
        self.island_client = island_client
        self.log_dir_path = log_dir_path
        self.monkey_log_paths = []

    def download_monkey_logs(self):
        LOGGER.info("Downloading each monkey log.")
        all_monkeys = self.island_client.get_all_monkeys_from_db()
        for monkey in all_monkeys:
            downloaded_log_path = self._download_monkey_log(monkey)
            if downloaded_log_path:
                self.monkey_log_paths.append(downloaded_log_path)

    def _download_monkey_log(self, monkey):
        log_handler = MonkeyLog(monkey, self.log_dir_path)
        download_successful = log_handler.download_log(self.island_client)
        return log_handler.get_log_path_for_monkey(monkey) if download_successful else None
