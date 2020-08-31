import logging
import os
import shutil

from envs.monkey_zoo.blackbox.log_handlers.monkey_log_parser import \
    MonkeyLogParser
from envs.monkey_zoo.blackbox.log_handlers.monkey_logs_downloader import \
    MonkeyLogsDownloader

LOG_DIR_NAME = 'logs'
LOGGER = logging.getLogger(__name__)


class TestLogsHandler(object):
    def __init__(self, test_name, island_client, log_dir_path):
        self.test_name = test_name
        self.island_client = island_client
        self.log_dir_path = os.path.join(log_dir_path, self.test_name)

    def parse_test_logs(self):
        log_paths = self.download_logs()
        if not log_paths:
            LOGGER.error("No logs were downloaded. Maybe no monkeys were ran "
                         "or early exception prevented log download?")
            return
        TestLogsHandler.parse_logs(log_paths)

    def download_logs(self):
        self.try_create_log_dir_for_test()
        downloader = MonkeyLogsDownloader(self.island_client, self.log_dir_path)
        downloader.download_monkey_logs()
        return downloader.monkey_log_paths

    def try_create_log_dir_for_test(self):
        try:
            os.mkdir(self.log_dir_path)
        except Exception as e:
            LOGGER.error("Can't create a dir for test logs: {}".format(e))

    @staticmethod
    def delete_log_folder_contents(log_dir_path):
        shutil.rmtree(log_dir_path, ignore_errors=True)
        os.mkdir(log_dir_path)

    @staticmethod
    def parse_logs(log_paths):
        for log_path in log_paths:
            LOGGER.info("Info from log at {}".format(log_path))
            log_parser = MonkeyLogParser(log_path)
            log_parser.print_errors()
            log_parser.print_warnings()
