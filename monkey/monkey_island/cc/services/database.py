import logging

from flask import jsonify

from monkey_island.cc.database import mongo

logger = logging.getLogger(__name__)


# NOTE: This service is being replaced a little at a time by repositories
class Database(object):
    def __init__(self):
        pass

    @staticmethod
    def reset_db(reset_config=True):
        logger.info("Resetting database")
        # We can't drop system collections.
        [
            Database.drop_collection(x)
            for x in mongo.db.collection_names()
            if Database._should_drop(x, reset_config)
        ]
        logger.info("DB was reset")
        return jsonify(status="OK")

    @staticmethod
    def _should_drop(collection: str, drop_config: bool) -> bool:
        return not collection.startswith("system.") and not collection.startswith("config")

    @staticmethod
    def drop_collection(collection_name: str):
        mongo.db[collection_name].drop()
        logger.info("Dropped collection {}".format(collection_name))
