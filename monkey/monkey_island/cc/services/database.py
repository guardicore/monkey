import logging

from flask import jsonify

from monkey_island.cc.database import mongo
from monkey_island.cc.models.attack.attack_mitigations import AttackMitigations
from monkey_island.cc.services.attack.attack_config import AttackConfig
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.post_breach_files import remove_PBA_files

logger = logging.getLogger(__name__)


class Database(object):
    def __init__(self):
        pass

    @staticmethod
    def reset_db():
        logger.info('Resetting database')
        remove_PBA_files()
        # We can't drop system collections.
        [Database.drop_collection(x) for x in mongo.db.collection_names() if not x.startswith('system.')
         and not x == AttackMitigations.COLLECTION_NAME]
        ConfigService.init_config()
        AttackConfig.reset_config()
        logger.info('DB was reset')
        return jsonify(status='OK')

    @staticmethod
    def drop_collection(collection_name: str):
        mongo.db[collection_name].drop()
        logger.info("Dropped collection {}".format(collection_name))

    @staticmethod
    def init_db():
        if not mongo.db.collection_names():
            Database.reset_db()
