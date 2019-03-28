import logging
from dpath import util
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
    Applies ATT&CK matrix to the monkey configuration
    :return:
    """
    attack_techniques = get_techniques()
    monkey_config = ConfigService.get_config(False, True, True)
    monkey_schema = ConfigService.get_config_schema()
    set_arrays(attack_techniques, monkey_config, monkey_schema)
    set_booleans(attack_techniques, monkey_config, monkey_schema)
    ConfigService.update_config(monkey_config, True)


def set_arrays(attack_techniques, monkey_config, monkey_schema):
    """
    Sets exploiters/scanners/PBAs and other array type fields according to ATT&CK matrix
    :param attack_techniques: ATT&CK techniques dict. Format: {'T1110': True, ...}
    :param monkey_config: Monkey island's configuration
    :param monkey_schema: Monkey configuration schema
    """
    for key, definition in monkey_schema['definitions'].items():
        for array_field in definition['anyOf']:
            # Go trough each attack technique used by exploiter/scanner/PBA
            if 'attack_techniques' not in array_field:
                continue
            for attack_technique in array_field['attack_techniques']:
                # Skip if exploiter is marked with not yet implemented technique
                if attack_technique not in attack_techniques:
                    continue
                # If exploiter's attack technique is disabled, disable the exploiter/scanner/PBA
                if not attack_techniques[attack_technique]:
                    r_alter_array(monkey_config, key, array_field['enum'][0], remove=True)
                    break
                # If exploiter's attack technique is enabled, enable the exploiter/scanner/PBA
                else:
                    r_alter_array(monkey_config, key, array_field['enum'][0], remove=False)


def set_booleans(attack_techniques, monkey_config, monkey_schema):
    """
    Sets exploiters/scanners/PBAs and other array type fields according to ATT&CK matrix
    :param attack_techniques: ATT&CK techniques dict. Format: {'T1110': True, ...}
    :param monkey_config: Monkey island's configuration
    :param monkey_schema: Monkey configuration schema
    """
    for key, value in monkey_schema['properties'].items():
        r_set_booleans([key], value, attack_techniques, monkey_config)


def r_set_booleans(path, value, attack_techniques, monkey_config):
    if isinstance(value, dict):
        dictionary = {}
        if 'type' in value and value['type'] == 'boolean' and 'attack_techniques' in value:
            set_bool_conf_val(path, should_enable_field(value['attack_techniques'], attack_techniques), monkey_config)
        elif 'properties' in value:
            dictionary = value['properties']
        else:
            dictionary = value
        for key, item in dictionary.items():
            path.append(key)
            r_set_booleans(path, item, attack_techniques, monkey_config)
    del path[-1]


def set_bool_conf_val(path, val, monkey_config):
    util.set(monkey_config, '/'.join(path), val)


def should_enable_field(field_techniques, users_techniques):
    for technique in field_techniques:
        if not users_techniques[technique]:
            return False
    return True


def r_alter_array(config_value, array_name, field, remove=True):
    if isinstance(config_value, dict):
        if array_name in config_value and isinstance(config_value[array_name], list):
            if remove and field in config_value[array_name]:
                config_value[array_name].remove(field)
            elif not remove and field not in config_value[array_name]:
                config_value[array_name].append(field)
        else:
            for prop in config_value.items():
                r_alter_array(prop[1], array_name, field, remove)


def get_techniques():
    """
    Parses ATT&CK config into a dic of techniques.
    :return: Dictionary of techniques. Format: {"T1110": True, "T1075": False, ...}
    """
    attack_config = get_config()
    techniques = {}
    for key, attack_type in attack_config['properties'].items():
        for key, technique in attack_type['properties'].items():
            techniques[key] = technique['value']
    return techniques
