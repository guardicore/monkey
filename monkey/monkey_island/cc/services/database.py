import logging

from flask import jsonify

from monkey_island.cc.database import mongo
from monkey_island.cc.models import Config
from monkey_island.cc.models.agent_controls import AgentControls
from monkey_island.cc.models.attack.attack_mitigations import AttackMitigations
from monkey_island.cc.models.island_mode_model import IslandMode
from monkey_island.cc.services.config import ConfigService

logger = logging.getLogger(__name__)


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
        ConfigService.init_config()
        Database.init_agent_controls()
        logger.info("DB was reset")
        return jsonify(status="OK")

    @staticmethod
    def _should_drop(collection: str, drop_config: bool) -> bool:
        if not drop_config:
            if collection == IslandMode.COLLECTION_NAME or collection == Config.COLLECTION_NAME:
                return False
        return (
            not collection.startswith("system.")
            and not collection == AttackMitigations.COLLECTION_NAME
        )

    @staticmethod
    def drop_collection(collection_name: str):
        mongo.db[collection_name].drop()
        logger.info("Dropped collection {}".format(collection_name))

    @staticmethod
    def init_agent_controls():
        AgentControls().save()

    @staticmethod
    def is_mitigations_missing() -> bool:
        return bool(AttackMitigations.COLLECTION_NAME not in mongo.db.list_collection_names())
