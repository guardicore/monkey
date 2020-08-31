import logging
import os

from bson import ObjectId

LOGGER = logging.getLogger(__name__)


class MonkeyLog(object):
    def __init__(self, monkey, log_dir_path):
        self.monkey = monkey
        self.log_dir_path = log_dir_path

    def download_log(self, island_client):
        log = island_client.find_log_in_db({'monkey_id': ObjectId(self.monkey['id'])})
        if not log:
            LOGGER.error("Log for monkey {} not found".format(self.monkey['ip_addresses'][0]))
            return False
        else:
            self.write_log_to_file(log)
            return True

    def write_log_to_file(self, log):
        with open(self.get_log_path_for_monkey(self.monkey), 'w') as log_file:
            log_file.write(MonkeyLog.parse_log(log))

    @staticmethod
    def parse_log(log):
        log = log.strip('"')
        log = log.replace("\\n", "\n ")
        return log

    @staticmethod
    def get_filename_for_monkey_log(monkey):
        return "{}.txt".format(monkey['ip_addresses'][0])

    def get_log_path_for_monkey(self, monkey):
        return os.path.join(self.log_dir_path, MonkeyLog.get_filename_for_monkey_log(monkey))
