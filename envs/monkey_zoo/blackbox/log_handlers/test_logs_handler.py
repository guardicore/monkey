import os
import shutil

from envs.monkey_zoo.blackbox.log_handlers.log_parser import LogParser
from envs.monkey_zoo.blackbox.log_handlers.logs_downloader import LogsDownloader

LOG_DIR_NAME = 'logs'


class TestLogsHandler(object):
    def __init__(self, test_name, island_client):
        self.test_name = test_name
        self.island_client = island_client
        self.log_dir_path = os.path.join(TestLogsHandler.get_log_dir_path(), self.test_name)

    def parse_test_logs(self):
        log_paths = self.download_logs()
        if not log_paths:
            print("No logs were downloaded, maybe no monkeys were ran?")
            return
        TestLogsHandler.parse_logs(log_paths)

    def download_logs(self):
        self.try_create_log_dir_for_test()
        downloader = LogsDownloader(self.island_client, self.log_dir_path)
        downloader.download_monkey_logs()
        return downloader.monkey_log_paths

    def try_create_log_dir_for_test(self):
        try:
            os.mkdir(self.log_dir_path)
        except Exception as e:
            print("Can't create a dir for test logs: {}".format(e))

    @staticmethod
    def get_log_dir_path():
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), LOG_DIR_NAME)

    @staticmethod
    def delete_log_folder_contents():
        shutil.rmtree(TestLogsHandler.get_log_dir_path(), ignore_errors=True)
        os.mkdir(TestLogsHandler.get_log_dir_path())

    @staticmethod
    def parse_logs(log_paths):
        for log_path in log_paths:
            print("Info from log at {}".format(log_path))
            log_parser = LogParser(log_path)
            log_parser.print_errors()
            log_parser.print_warnings()
