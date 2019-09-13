import os
import shutil

from envs.monkey_zoo.blackbox.log_handlers.monkey_log import MonkeyLog

LOG_DIR_NAME = 'logs'


class TestLogsHandler(object):
    def __init__(self, test_name, island_client):
        self.test_name = test_name
        self.island_client = island_client
        self.log_dir_path = os.path.join(TestLogsHandler.get_log_dir_path(), self.test_name)

    def download_logs(self):
        self.try_create_log_dir_for_test()
        print("Downloading logs")
        all_monkeys = self.island_client.find_monkeys_in_db(None)
        for monkey in all_monkeys:
            MonkeyLog(monkey, self.log_dir_path).download_log(self.island_client)

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
