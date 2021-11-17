import logging

from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.attack_schema import SCHEMA

logger = logging.getLogger(__name__)


class AttackConfig(object):
    def __init__(self):
        pass

    @staticmethod
    def get_config():
        config = mongo.db.attack.find_one({"name": "newconfig"})["properties"]
        return config

    @staticmethod
    def get_technique(technique_id):
        """
        Gets technique by id
        :param technique_id: E.g. T1210
        :return: Technique object or None if technique is not found
        """
        attack_config = AttackConfig.get_config()
        for config_key, attack_type in list(attack_config.items()):
            for type_key, technique in list(attack_type["properties"].items()):
                if type_key == technique_id:
                    return technique
        return None

    @staticmethod
    def reset_config():
        AttackConfig.update_config(SCHEMA)

    @staticmethod
    def update_config(config_json):
        mongo.db.attack.update({"name": "newconfig"}, {"$set": config_json}, upsert=True)
        return True

    @staticmethod
    def get_technique_values():
        """
        Parses ATT&CK config into a dict of techniques and corresponding values.
        :return: Dictionary of techniques. Format: {"T1110": True, "T1075": False, ...}
        """
        attack_config = AttackConfig.get_config()
        techniques = {}
        for type_name, attack_type in list(attack_config.items()):
            for key, technique in list(attack_type["properties"].items()):
                techniques[key] = technique["value"]
        return techniques

    @staticmethod
    def get_techniques_for_report():
        """
        :return: Format: {"T1110": {"selected": True, "type": "Credential Access", "T1075": ...}
        """
        attack_config = AttackConfig.get_config()
        techniques = {}
        for type_name, attack_type in list(attack_config.items()):
            for key, technique in list(attack_type["properties"].items()):
                techniques[key] = {
                    "selected": technique["value"],
                    "type": SCHEMA["properties"][type_name]["title"],
                }
        return techniques
