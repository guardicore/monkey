import logging
from cc.database import mongo
from attck_schema import SCHEMA
from jsonschema import Draft4Validator, validators

__author__ = "VakarisZ"

logger = logging.getLogger(__name__)


class AttckService:
    default_config = None

    def __init__(self):
        pass

    @staticmethod
    def get_config():
        config = mongo.db.attck.find_one({'name': 'newconfig'}) or AttckService.get_default_config()
        return config

    @staticmethod
    def get_config_schema():
        return SCHEMA

    @staticmethod
    def reset_config():
        config = AttckService.get_default_config()
        AttckService.update_config(config)
        logger.info('Monkey config reset was called')

    @staticmethod
    def update_config(config_json):
        mongo.db.attck.update({'name': 'newconfig'}, {"$set": config_json}, upsert=True)
        logger.info('Attck config was updated')
        return True

    @staticmethod
    def get_default_config():
        if not AttckService.default_config:
            AttckService.update_config(SCHEMA)
            AttckService.default_config = SCHEMA
        return AttckService.default_config
