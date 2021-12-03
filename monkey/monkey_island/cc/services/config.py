import collections
import copy
import functools
import logging
from typing import Dict

from jsonschema import Draft4Validator, validators

from common.config_value_paths import (
    AWS_KEYS_PATH,
    EXPORT_MONKEY_TELEMS_PATH,
    LM_HASH_LIST_PATH,
    NTLM_HASH_LIST_PATH,
    PASSWORD_LIST_PATH,
    PBA_LINUX_FILENAME_PATH,
    PBA_WINDOWS_FILENAME_PATH,
    SSH_KEYS_PATH,
    STARTED_ON_ISLAND_PATH,
    USER_LIST_PATH,
)
from monkey_island.cc.database import mongo
from monkey_island.cc.server_utils.consts import ISLAND_PORT
from monkey_island.cc.server_utils.encryption import get_datastore_encryptor
from monkey_island.cc.services.config_manipulator import update_config_per_mode
from monkey_island.cc.services.config_schema.config_schema import SCHEMA
from monkey_island.cc.services.mode.island_mode_service import ModeNotSetError, get_mode
from monkey_island.cc.services.post_breach_files import PostBreachFilesService
from monkey_island.cc.services.utils.network_utils import local_ip_addresses

logger = logging.getLogger(__name__)

# This should be used for config values of array type (array of strings only)
ENCRYPTED_CONFIG_VALUES = [
    PASSWORD_LIST_PATH,
    LM_HASH_LIST_PATH,
    NTLM_HASH_LIST_PATH,
    SSH_KEYS_PATH,
    AWS_KEYS_PATH + ["aws_access_key_id"],
    AWS_KEYS_PATH + ["aws_secret_access_key"],
    AWS_KEYS_PATH + ["aws_session_token"],
]


class ConfigService:
    default_config = None

    def __init__(self):
        pass

    @staticmethod
    def get_config(is_initial_config=False, should_decrypt=True, is_island=False):
        """
        Gets the entire global config.
        :param is_initial_config: If True, the initial config will be returned instead of the
        current config.
        :param should_decrypt: If True, all config values which are set as encrypted will be
        decrypted.
        :param is_island: If True, will include island specific configuration parameters.
        :return: The entire global config.
        """
        config = (
            mongo.db.config.find_one({"name": "initial" if is_initial_config else "newconfig"})
            or {}
        )
        for field in ("name", "_id"):
            config.pop(field, None)
        if should_decrypt and len(config) > 0:
            ConfigService.decrypt_config(config)
        if not is_island:
            config.get("cnc", {}).pop("aws_config", None)
        return config

    @staticmethod
    def get_config_value(config_key_as_arr, is_initial_config=False, should_decrypt=True):
        """
        Get a specific config value.
        :param config_key_as_arr: The config key as an array. e.g. ['basic', 'credentials',
        'exploit_password_list'].
        :param is_initial_config: If True, returns the value of the initial config instead of the
        current config.
        :param should_decrypt: If True, the value of the config key will be decrypted
                               (if it's in the list of encrypted config values).
        :return: The value of the requested config key.
        """
        config_key = functools.reduce(lambda x, y: x + "." + y, config_key_as_arr)
        config = mongo.db.config.find_one(
            {"name": "initial" if is_initial_config else "newconfig"}, {config_key: 1}
        )
        for config_key_part in config_key_as_arr:
            config = config[config_key_part]
        if should_decrypt:
            if config_key_as_arr in ENCRYPTED_CONFIG_VALUES:
                if isinstance(config, str):
                    config = get_datastore_encryptor().decrypt(config)
                elif isinstance(config, list):
                    config = [get_datastore_encryptor().decrypt(x) for x in config]
        return config

    @staticmethod
    def set_config_value(config_key_as_arr, value):
        mongo_key = ".".join(config_key_as_arr)
        mongo.db.config.update({"name": "newconfig"}, {"$set": {mongo_key: value}})

    @staticmethod
    def get_flat_config(is_initial_config=False, should_decrypt=True):
        config_json = ConfigService.get_config(is_initial_config, should_decrypt)
        flat_config_json = {}
        for i in config_json:
            if i == "ransomware":
                # Don't flatten the ransomware because ransomware payload expects a dictionary #1260
                flat_config_json[i] = config_json[i]
                continue
            for j in config_json[i]:
                for k in config_json[i][j]:
                    if isinstance(config_json[i][j][k], dict):
                        for key, value in config_json[i][j][k].items():
                            flat_config_json[key] = value
                    else:
                        flat_config_json[k] = config_json[i][j][k]

        return flat_config_json

    @staticmethod
    def get_config_schema():
        return SCHEMA

    @staticmethod
    def add_item_to_config_set_if_dont_exist(item_path_array, item_value, should_encrypt):
        item_key = ".".join(item_path_array)
        items_from_config = ConfigService.get_config_value(item_path_array, False, should_encrypt)
        if item_value in items_from_config:
            return
        if should_encrypt:
            item_value = get_datastore_encryptor().encrypt(item_value)
        mongo.db.config.update(
            {"name": "newconfig"}, {"$addToSet": {item_key: item_value}}, upsert=False
        )

        mongo.db.monkey.update(
            {}, {"$addToSet": {"config." + item_key.split(".")[-1]: item_value}}, multi=True
        )

    @staticmethod
    def creds_add_username(username):
        ConfigService.add_item_to_config_set_if_dont_exist(
            USER_LIST_PATH, username, should_encrypt=False
        )

    @staticmethod
    def creds_add_password(password):
        ConfigService.add_item_to_config_set_if_dont_exist(
            PASSWORD_LIST_PATH, password, should_encrypt=True
        )

    @staticmethod
    def creds_add_lm_hash(lm_hash):
        ConfigService.add_item_to_config_set_if_dont_exist(
            LM_HASH_LIST_PATH, lm_hash, should_encrypt=True
        )

    @staticmethod
    def creds_add_ntlm_hash(ntlm_hash):
        ConfigService.add_item_to_config_set_if_dont_exist(
            NTLM_HASH_LIST_PATH, ntlm_hash, should_encrypt=True
        )

    @staticmethod
    def ssh_add_keys(public_key, private_key, user, ip):
        if not ConfigService.ssh_key_exists(
            ConfigService.get_config_value(SSH_KEYS_PATH, False, False), user, ip
        ):
            ConfigService.add_item_to_config_set_if_dont_exist(
                SSH_KEYS_PATH,
                {"public_key": public_key, "private_key": private_key, "user": user, "ip": ip},
                # SSH keys already encrypted in process_ssh_info()
                should_encrypt=False,
            )

    @staticmethod
    def ssh_key_exists(keys, user, ip):
        return [key for key in keys if key["user"] == user and key["ip"] == ip]

    def _filter_none_values(data):
        if isinstance(data, dict):
            return {
                k: ConfigService._filter_none_values(v)
                for k, v in data.items()
                if k is not None and v is not None
            }
        elif isinstance(data, list):
            return [ConfigService._filter_none_values(item) for item in data if item is not None]
        else:
            return data

    @staticmethod
    def update_config(config_json, should_encrypt):
        # PBA file upload happens on pba_file_upload endpoint and corresponding config options
        # are set there
        config_json = ConfigService._filter_none_values(config_json)
        ConfigService.set_config_PBA_files(config_json)
        if should_encrypt:
            try:
                ConfigService.encrypt_config(config_json)
            except KeyError:
                logger.error("Bad configuration file was submitted.")
                return False
        mongo.db.config.update({"name": "newconfig"}, {"$set": config_json}, upsert=True)
        logger.info("monkey config was updated")
        return True

    @staticmethod
    def set_config_PBA_files(config_json):
        """
        Sets PBA file info in config_json to current config's PBA file info values.
        :param config_json: config_json that will be modified
        """
        if ConfigService.get_config():
            linux_filename = ConfigService.get_config_value(PBA_LINUX_FILENAME_PATH)
            windows_filename = ConfigService.get_config_value(PBA_WINDOWS_FILENAME_PATH)

            ConfigService.set_config_value(PBA_LINUX_FILENAME_PATH, linux_filename)
            ConfigService.set_config_value(PBA_WINDOWS_FILENAME_PATH, windows_filename)

    @staticmethod
    def init_default_config():
        if ConfigService.default_config is None:
            default_validating_draft4_validator = ConfigService._extend_config_with_default(
                Draft4Validator
            )
            config = {}
            default_validating_draft4_validator(SCHEMA).validate(config)
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
        PostBreachFilesService.remove_PBA_files()
        config = ConfigService.get_default_config(True)
        ConfigService.set_server_ips_in_config(config)
        try:
            mode = get_mode()
            update_config_per_mode(mode, config, should_encrypt=False)
        except ModeNotSetError:
            ConfigService.update_config(config, should_encrypt=False)
        logger.info("Monkey config reset was called")

    @staticmethod
    def set_server_ips_in_config(config):
        ips = local_ip_addresses()
        config["internal"]["island_server"]["command_servers"] = [
            "%s:%d" % (ip, ISLAND_PORT) for ip in ips
        ]
        config["internal"]["island_server"]["current_server"] = "%s:%d" % (
            ips[0],
            ISLAND_PORT,
        )

    @staticmethod
    def save_initial_config_if_needed():
        if mongo.db.config.find_one({"name": "initial"}) is not None:
            return

        initial_config = mongo.db.config.find_one({"name": "newconfig"})
        initial_config["name"] = "initial"
        initial_config.pop("_id")
        mongo.db.config.insert(initial_config)
        logger.info("Monkey config was inserted to mongo and saved")

    @staticmethod
    def _extend_config_with_default(validator_class):
        validate_properties = validator_class.VALIDATORS["properties"]

        def set_defaults(validator, properties, instance, schema):
            # Do it only for root.
            if instance != {}:
                return
            for property1, subschema1 in list(properties.items()):
                main_dict = {}
                for property2, subschema2 in list(subschema1["properties"].items()):
                    sub_dict = {}
                    for property3, subschema3 in list(subschema2["properties"].items()):
                        if "default" in subschema3:
                            sub_dict[property3] = subschema3["default"]
                        elif "properties" in subschema3:
                            layer_3_dict = {}
                            for property4, subschema4 in list(subschema3["properties"].items()):
                                if "properties" in subschema4:
                                    raise ValueError(
                                        "monkey/monkey_island/cc/services/config.py "
                                        "can't handle 5 level config. "
                                        "Either change back the config or refactor."
                                    )
                                if "default" in subschema4:
                                    layer_3_dict[property4] = subschema4["default"]
                            sub_dict[property3] = layer_3_dict
                    main_dict[property2] = sub_dict
                instance.setdefault(property1, main_dict)

            for error in validate_properties(validator, properties, instance, schema):
                yield error

        return validators.extend(
            validator_class,
            {"properties": set_defaults},
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
        keys = [config_arr_as_array[-1] for config_arr_as_array in ENCRYPTED_CONFIG_VALUES]

        for key in keys:
            if isinstance(flat_config[key], collections.Sequence) and not isinstance(
                flat_config[key], str
            ):
                # Check if we are decrypting ssh key pair
                if (
                    flat_config[key]
                    and isinstance(flat_config[key][0], dict)
                    and "public_key" in flat_config[key][0]
                ):
                    flat_config[key] = [
                        ConfigService.decrypt_ssh_key_pair(item) for item in flat_config[key]
                    ]
                else:
                    flat_config[key] = [
                        get_datastore_encryptor().decrypt(item) for item in flat_config[key]
                    ]
            else:
                flat_config[key] = get_datastore_encryptor().decrypt(flat_config[key])
        return flat_config

    @staticmethod
    def _encrypt_or_decrypt_config(config, is_decrypt=False):
        for config_arr_as_array in ENCRYPTED_CONFIG_VALUES:
            config_arr = config
            parent_config_arr = None

            # Because the config isn't flat, this for-loop gets the actual config value out of
            # the config
            for config_key_part in config_arr_as_array:
                parent_config_arr = config_arr
                config_arr = config_arr[config_key_part]

            if isinstance(config_arr, collections.abc.Sequence) and not isinstance(config_arr, str):
                for i in range(len(config_arr)):
                    # Check if array of shh key pairs and then decrypt
                    if isinstance(config_arr[i], dict) and "public_key" in config_arr[i]:
                        config_arr[i] = (
                            ConfigService.decrypt_ssh_key_pair(config_arr[i])
                            if is_decrypt
                            else ConfigService.decrypt_ssh_key_pair(config_arr[i], True)
                        )
                    else:
                        config_arr[i] = (
                            get_datastore_encryptor().decrypt(config_arr[i])
                            if is_decrypt
                            else get_datastore_encryptor().encrypt(config_arr[i])
                        )
            else:
                parent_config_arr[config_arr_as_array[-1]] = (
                    get_datastore_encryptor().decrypt(config_arr)
                    if is_decrypt
                    else get_datastore_encryptor().encrypt(config_arr)
                )

    @staticmethod
    def decrypt_ssh_key_pair(pair, encrypt=False):
        if encrypt:
            pair["public_key"] = get_datastore_encryptor().encrypt(pair["public_key"])
            pair["private_key"] = get_datastore_encryptor().encrypt(pair["private_key"])
        else:
            pair["public_key"] = get_datastore_encryptor().decrypt(pair["public_key"])
            pair["private_key"] = get_datastore_encryptor().decrypt(pair["private_key"])
        return pair

    @staticmethod
    def is_test_telem_export_enabled():
        return ConfigService.get_config_value(EXPORT_MONKEY_TELEMS_PATH)

    @staticmethod
    def set_started_on_island(value: bool):
        ConfigService.set_config_value(STARTED_ON_ISLAND_PATH, value)

    @staticmethod
    def get_config_propagation_credentials():
        return {
            "exploit_user_list": ConfigService.get_config_value(
                USER_LIST_PATH, should_decrypt=False
            ),
            "exploit_password_list": ConfigService.get_config_value(
                PASSWORD_LIST_PATH, should_decrypt=False
            ),
            "exploit_lm_hash_list": ConfigService.get_config_value(
                LM_HASH_LIST_PATH, should_decrypt=False
            ),
            "exploit_ntlm_hash_list": ConfigService.get_config_value(
                NTLM_HASH_LIST_PATH, should_decrypt=False
            ),
            "exploit_ssh_keys": ConfigService.get_config_value(SSH_KEYS_PATH, should_decrypt=False),
        }

    @staticmethod
    def format_flat_config_for_agent(config: Dict):
        ConfigService._remove_credentials_from_flat_config(config)

    @staticmethod
    def _remove_credentials_from_flat_config(config: Dict):
        fields_to_remove = {
            "exploit_lm_hash_list",
            "exploit_ntlm_hash_list",
            "exploit_password_list",
            "exploit_ssh_keys",
            "exploit_user_list",
        }

        for field in fields_to_remove:
            config.pop(field, None)
