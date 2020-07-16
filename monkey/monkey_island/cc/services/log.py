from datetime import datetime

import monkey_island.cc.services.node
from monkey_island.cc.database import database, mongo

__author__ = "itay.mizeretz"


class LogService:
    def __init__(self):
        pass

    @staticmethod
    def get_log_by_monkey_id(monkey_id):
        log = mongo.db.log.find_one({'monkey_id': monkey_id})
        if log:
            log_file = database.gridfs.get(log['file_id'])
            monkey_label = monkey_island.cc.services.node.NodeService.get_monkey_label(
                monkey_island.cc.services.node.NodeService.get_monkey_by_id(log['monkey_id']))
            return \
                {
                    'monkey_label': monkey_label,
                    'log': log_file.read().decode(),
                    'timestamp': log['timestamp']
                }

    @staticmethod
    def remove_logs_by_monkey_id(monkey_id):
        log = mongo.db.log.find_one({'monkey_id': monkey_id})
        if log is not None:
            database.gridfs.delete(log['file_id'])
            mongo.db.log.delete_one({'monkey_id': monkey_id})

    @staticmethod
    def add_log(monkey_id, log_data, timestamp=datetime.now()):
        LogService.remove_logs_by_monkey_id(monkey_id)
        file_id = database.gridfs.put(log_data, encoding='utf-8')
        return mongo.db.log.insert(
            {
                'monkey_id': monkey_id,
                'file_id': file_id,
                'timestamp': timestamp
            }
        )

    @staticmethod
    def log_exists(monkey_id):
        return mongo.db.log.find_one({'monkey_id': monkey_id}) is not None
