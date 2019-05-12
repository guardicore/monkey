import copy
import collections
import functools
import logging
from jsonschema import Draft4Validator, validators
from six import string_types
import monkey_island.cc.services.post_breach_files

from monkey_island.cc.database import mongo
from monkey_island.cc.encryptor import encryptor
from monkey_island.cc.environment.environment import env
from monkey_island.cc.utils import local_ip_addresses
from config_schema import SCHEMA

__author__ = "itay.mizeretz"

logger = logging.getLogger(__name__)


# This should be used for config values of array type (array of strings only)
ENCRYPTED_CONFIG_ARRAYS = \
    [
        ['basic', 'credentials', 'exploit_password_list'],
        ['internal', 'exploits', 'exploit_lm_hash_list'],
        ['internal', 'exploits', 'exploit_ntlm_hash_list'],
        ['internal', 'exploits', 'exploit_ssh_keys']
    ]


class ConfigService:
    default_config = None

    def __init__(self):
        pass

    @staticmethod
    def get_config(is_initial_config=False, should_decrypt=True, is_island=False):
        """
        Gets the entire global config.
        :param is_initial_config: If True, the initial config will be returned instead of the current config.
        :param should_decrypt: If True, all config values which are set as encrypted will be decrypted.
        :param is_island: If True, will include island specific configuration parameters.
        :return: The entire global config.
        """
        config = mongo.db.config.find_one({'name': 'initial' if is_initial_config else 'newconfig'}) or {}
        for field in ('name', '_id'):
            config.pop(field, None)
        if should_decrypt and len(config) > 0:
            ConfigService.decrypt_config(config)
        if not is_island:
            config.get('cnc', {}).pop('aws_config', None)
        return config

    @staticmethod
    def get_config_value(config_key_as_arr, is_initial_config=False, should_decrypt=True):
        """
        Get a specific config value.
        :param config_key_as_arr: The config key as an array. e.g. ['basic', 'credentials', 'exploit_password_list'].
        :param is_initial_config: If True, returns the value of the initial config instead of the current config.
        :param should_decrypt: If True, the value of the config key will be decrypted
                               (if it's in the list of encrypted config values).
        :return: The value of the requested config key.
        """
        config_key = functools.reduce(lambda x, y: x + '.' + y, config_key_as_arr)
        config = mongo.db.config.find_one({'name': 'initial' if is_initial_config else 'newconfig'}, {config_key: 1})
        for config_key_part in config_key_as_arr:
            config = config[config_key_part]
        if should_decrypt:
            if config_key_as_arr in ENCRYPTED_CONFIG_ARRAYS:
                config = [encryptor.dec(x) for x in config]
        return config

    @staticmethod
    def set_config_value(config_key_as_arr, value):
        mongo_key = ".".join(config_key_as_arr)
        mongo.db.config.update({'name': 'newconfig'},
                               {"$set": {mongo_key: value}})

    @staticmethod
    def get_flat_config(is_initial_config=False, should_decrypt=True):
        config_json = ConfigService.get_config(is_initial_config, should_decrypt)
        flat_config_json = {}
        for i in config_json:
            for j in config_json[i]:
                for k in config_json[i][j]:
                    flat_config_json[k] = config_json[i][j][k]

        return flat_config_json

    @staticmethod
    def get_config_schema():
        return SCHEMA

    @staticmethod
    def add_item_to_config_set(item_key, item_value):
        mongo.db.config.update(
            {'name': 'newconfig'},
            {'$addToSet': {item_key: item_value}},
            upsert=False
        )

        mongo.db.monkey.update(
            {},
            {'$addToSet': {'config.' + item_key.split('.')[-1]: item_value}},
            multi=True
        )

    @staticmethod
    def creds_add_username(username):
        ConfigService.add_item_to_config_set('basic.credentials.exploit_user_list', username)

    @staticmethod
    def creds_add_password(password):
        ConfigService.add_item_to_config_set('basic.credentials.exploit_password_list', password)

    @staticmethod
    def creds_add_lm_hash(lm_hash):
        ConfigService.add_item_to_config_set('internal.exploits.exploit_lm_hash_list', lm_hash)

    @staticmethod
    def creds_add_ntlm_hash(ntlm_hash):
        ConfigService.add_item_to_config_set('internal.exploits.exploit_ntlm_hash_list', ntlm_hash)

    @staticmethod
    def ssh_add_keys(public_key, private_key, user, ip):
        if not ConfigService.ssh_key_exists(ConfigService.get_config_value(['internal', 'exploits', 'exploit_ssh_keys'],
                                                                           False, False), user, ip):
            ConfigService.add_item_to_config_set('internal.exploits.exploit_ssh_keys',
                                             {"public_key": public_key, "private_key": private_key,
                                              "user": user, "ip": ip})

    @staticmethod
    def ssh_key_exists(keys, user, ip):
        return [key for key in keys if key['user'] == user and key['ip'] == ip]

    @staticmethod
    def update_config(config_json, should_encrypt):
        # PBA file upload happens on pba_file_upload endpoint and corresponding config options are set there
        monkey_island.cc.services.post_breach_files.set_config_PBA_files(config_json)
        if should_encrypt:
            try:
                ConfigService.encrypt_config(config_json)
            except KeyError as e:
                logger.error('Bad configuration file was submitted.')
                return False
        mongo.db.config.update({'name': 'newconfig'}, {"$set": config_json}, upsert=True)
        logger.info('monkey config was updated')
        return True

    @staticmethod
    def init_default_config():
        if ConfigService.default_config is None:
            defaultValidatingDraft4Validator = ConfigService._extend_config_with_default(Draft4Validator)
            config = {}
            defaultValidatingDraft4Validator(SCHEMA).validate(config)
            ConfigService.default_config = config

    @staticmethod
    def get_default_config(should_encrypt=False):
        ConfigService.init_default_config()
        config = copy.deepcopy(ConfigService.default_config)
        if should_encrypt:
            ConfigService.encrypt_config(config)
        logger.info("Default config was called")
        return config

    @staticmethod
    def init_config():
        if ConfigService.get_config(should_decrypt=False) != {}:
            return
        ConfigService.reset_config()

    @staticmethod
    def reset_config():
        monkey_island.cc.services.post_breach_files.remove_PBA_files()
        config = ConfigService.get_default_config(True)
        ConfigService.set_server_ips_in_config(config)
        ConfigService.update_config(config, should_encrypt=False)
        logger.info('Monkey config reset was called')

    @staticmethod
    def set_server_ips_in_config(config):
        ips = local_ip_addresses()
        config["cnc"]["servers"]["command_servers"] = ["%s:%d" % (ip, env.get_island_port()) for ip in ips]
        config["cnc"]["servers"]["current_server"] = "%s:%d" % (ips[0], env.get_island_port())

    @staticmethod
    def save_initial_config_if_needed():
        if mongo.db.config.find_one({'name': 'initial'}) is not None:
            return

        initial_config = mongo.db.config.find_one({'name': 'newconfig'})
        initial_config['name'] = 'initial'
        initial_config.pop('_id')
        mongo.db.config.insert(initial_config)
        logger.info('Monkey config was inserted to mongo and saved')

    @staticmethod
    def _extend_config_with_default(validator_class):
        validate_properties = validator_class.VALIDATORS["properties"]

        def set_defaults(validator, properties, instance, schema):
            # Do it only for root.
            if instance != {}:
                return
            for property, subschema in properties.iteritems():
                main_dict = {}
                for property2, subschema2 in subschema["properties"].iteritems():
                    sub_dict = {}
                    for property3, subschema3 in subschema2["properties"].iteritems():
                        if "default" in subschema3:
                            sub_dict[property3] = subschema3["default"]
                    main_dict[property2] = sub_dict
                instance.setdefault(property, main_dict)

            for error in validate_properties(validator, properties, instance, schema):
                yield error

        return validators.extend(
            validator_class, {"properties": set_defaults},
        )

    @staticmethod
    def decrypt_config(config):
        ConfigService._encrypt_or_decrypt_config(config, True)

    @staticmethod
    def encrypt_config(config):
        ConfigService._encrypt_or_decrypt_config(config, False)

    @staticmethod
    def decrypt_flat_config(flat_config, is_island=False):
        """
        Same as decrypt_config but for a flat configuration
        """
        keys = [config_arr_as_array[2] for config_arr_as_array in ENCRYPTED_CONFIG_ARRAYS]

        for key in keys:
            if isinstance(flat_config[key], collections.Sequence) and not isinstance(flat_config[key], string_types):
                # Check if we are decrypting ssh key pair
                if flat_config[key] and isinstance(flat_config[key][0], dict) and 'public_key' in flat_config[key][0]:
                    flat_config[key] = [ConfigService.decrypt_ssh_key_pair(item) for item in flat_config[key]]
                else:
                    flat_config[key] = [encryptor.dec(item) for item in flat_config[key]]
            else:
                flat_config[key] = encryptor.dec(flat_config[key])
        return flat_config

    @staticmethod
    def _encrypt_or_decrypt_config(config, is_decrypt=False):
        for config_arr_as_array in ENCRYPTED_CONFIG_ARRAYS:
            config_arr = config
            parent_config_arr = None

            # Because the config isn't flat, this for-loop gets the actual config value out of the config
            for config_key_part in config_arr_as_array:
                parent_config_arr = config_arr
                config_arr = config_arr[config_key_part]

            if isinstance(config_arr, collections.Sequence) and not isinstance(config_arr, string_types):
                for i in range(len(config_arr)):
                    # Check if array of shh key pairs and then decrypt
                    if isinstance(config_arr[i], dict) and 'public_key' in config_arr[i]:
                        config_arr[i] = ConfigService.decrypt_ssh_key_pair(config_arr[i]) if is_decrypt else \
                                        ConfigService.decrypt_ssh_key_pair(config_arr[i], True)
                    else:
                        config_arr[i] = encryptor.dec(config_arr[i]) if is_decrypt else encryptor.enc(config_arr[i])
            else:
                parent_config_arr[config_arr_as_array[-1]] =\
                    encryptor.dec(config_arr) if is_decrypt else encryptor.enc(config_arr)

    @staticmethod
    def decrypt_ssh_key_pair(pair, encrypt=False):
        if encrypt:
            pair['public_key'] = encryptor.enc(pair['public_key'])
            pair['private_key'] = encryptor.enc(pair['private_key'])
        else:
            pair['public_key'] = encryptor.dec(pair['public_key'])
            pair['private_key'] = encryptor.dec(pair['private_key'])
        return pair
