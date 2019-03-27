import logging
from cc.database import mongo
from attack_schema import SCHEMA
from cc.services.config import ConfigService

__author__ = "VakarisZ"

logger = logging.getLogger(__name__)


def get_config():
    config = mongo.db.attack.find_one({'name': 'newconfig'}) or reset_config()
    return config


def get_config_schema():
    return SCHEMA


def reset_config():
    update_config(SCHEMA)


def update_config(config_json):
    mongo.db.attack.update({'name': 'newconfig'}, {"$set": config_json}, upsert=True)
    return True


def apply_to_monkey_config():
    """
    Applies ATT&CK matrix in the database to the monkey configuration
    :return:
    """
    attack_techniques = get_techniques()
    monkey_config = ConfigService.get_config(False, True, True)
    monkey_schema = ConfigService.get_config_schema()
    set_exploiters(attack_techniques, monkey_config, monkey_schema)
    ConfigService.update_config(monkey_config, True)


def set_exploiters(attack_techniques, monkey_config, monkey_schema):
    """
    Sets exploiters according to ATT&CK matrix
    :param attack_techniques: ATT&CK techniques dict. Format: {'T1110': True, ...}
    :param monkey_config: Monkey island's configuration
    :param monkey_schema: Monkey configuration schema
    """
    for exploiter in monkey_schema['definitions']['exploiter_classes']['anyOf']:
        # Go trough each attack technique used by exploiter
        for attack_technique in exploiter['attack_techniques']:
            # If exploiter's attack technique is disabled, disable the exploiter
            if not attack_techniques[attack_technique]:
                remove_exploiter(exploiter['enum'][0], monkey_config)
                break
            # If exploiter's attack technique is enabled, enable the exploiter
            else:
                add_exploiter(exploiter['enum'][0], monkey_config)


def remove_exploiter(exploiter, monkey_config):
    """
    Removes exploiter from monkey's configuration
    :param exploiter: Exploiter class name found in SCHEMA->definitions->exploiter_classes -> anyOf -> enum
    :param monkey_config: Monkey's configuration
    """
    if exploiter in monkey_config['exploits']['general']['exploiter_classes']:
        monkey_config['exploits']['general']['exploiter_classes'].remove(exploiter)


def add_exploiter(exploiter, monkey_config):
    """
    Adds exploiter to monkey's configuration
    :param exploiter: Exploiter class name found in SCHEMA->definitions->exploiter_classes -> anyOf -> enum
    :param monkey_config: Monkey's configuration
    """
    if not exploiter in monkey_config['exploits']['general']['exploiter_classes']:
        monkey_config['exploits']['general']['exploiter_classes'].append(exploiter)


def get_techniques():
    attack_config = get_config()
    techniques = {}
    for key, attack_type in attack_config['properties'].items():
        for key, technique in attack_type['properties'].items():
            techniques[key] = technique['value']
    return techniques
