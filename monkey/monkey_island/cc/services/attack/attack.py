import logging
from cc.database import mongo
from attack_schema import SCHEMA

__author__ = "VakarisZ"

logger = logging.getLogger(__name__)


class AttackService:
    default_config = None

    def __init__(self):
        pass

    @staticmethod
    def get_config():
        config = mongo.db.attack.find_one({'name': 'newconfig'}) or AttackService.get_default_config()
        return config

    @staticmethod
    def get_config_schema():
        return SCHEMA

    @staticmethod
    def reset_config():
        config = AttackService.get_default_config()
        AttackService.update_config(config)

    @staticmethod
    def update_config(config_json):
        mongo.db.attack.update({'name': 'newconfig'}, {"$set": config_json}, upsert=True)
        return True

    @staticmethod
    def parse_users_matrix(data):
        pass

    @staticmethod
    def get_default_config():
        if not AttackService.default_config:
            AttackService.update_config(SCHEMA)
            AttackService.default_config = SCHEMA
        return AttackService.default_config
