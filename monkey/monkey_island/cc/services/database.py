import logging

from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.attack.attack_config import AttackConfig
from monkey_island.cc.services.post_breach_files import remove_PBA_files
from flask import jsonify
from monkey_island.cc.database import mongo


logger = logging.getLogger(__name__)


class Database(object):
    def __init__(self):
        pass

    @staticmethod
    def reset_db():
        remove_PBA_files()
        # We can't drop system collections.
        [mongo.db[x].drop() for x in mongo.db.collection_names() if not x.startswith('system.')]
        ConfigService.init_config()
        AttackConfig.reset_config()
        logger.info('DB was reset')
        return jsonify(status='OK')

    @staticmethod
    def init_db():
        if not mongo.db.collection_names():
            Database.reset_db()

