import collections
import functools
import logging
from typing import Dict, List

from jsonschema import validators

from common.config_value_paths import (
    LM_HASH_LIST_PATH,
    NTLM_HASH_LIST_PATH,
    PASSWORD_LIST_PATH,
    PBA_LINUX_FILENAME_PATH,
    PBA_WINDOWS_FILENAME_PATH,
    SSH_KEYS_PATH,
    USER_LIST_PATH,
)
from monkey_island.cc.database import mongo
from monkey_island.cc.server_utils.encryption import (
    SensitiveField,
    StringEncryptor,
    decrypt_dict,
    encrypt_dict,
    get_datastore_encryptor,
)

logger = logging.getLogger(__name__)

# This should be used for config values of array type (array of strings only)
ENCRYPTED_CONFIG_VALUES = [
    PASSWORD_LIST_PATH,
    LM_HASH_LIST_PATH,
    NTLM_HASH_LIST_PATH,
    SSH_KEYS_PATH,
]

SENSITIVE_SSH_KEY_FIELDS = [
    SensitiveField(path="private_key", field_encryptor=StringEncryptor),
    SensitiveField(path="public_key", field_encryptor=StringEncryptor),
]


class ConfigService:
    default_config = None

    def __init__(self):
        pass

    @staticmethod
    def get_config(should_decrypt=True, is_island=False):
        """
        Gets the entire global config.

        :param should_decrypt: If True, all config values which are set as encrypted will be \
         decrypted. \
        :param is_island: If True, will include island specific configuration parameters. \
        :return: The entire global config.
        """

        # is_initial_config and should_decrypt are only there to compare if we are on the
        # default configuration or did user modified it already
        config = mongo.db.config.find_one() or {}
        config.pop("_id", None)
        if should_decrypt and len(config) > 0:
            ConfigService.decrypt_config(config)
        if not is_island:
            config.get("cnc", {}).pop("aws_config", None)
        return config

    @staticmethod
    def get_config_value(config_key_as_arr, should_decrypt=True):
        """
        Get a specific config value.

        :param config_key_as_arr: The config key as an array.
         e.g. ['basic', 'credentials','exploit_password_list'].
        :param should_decrypt: If True, the value of the config key will be decrypted
                               (if it's in the list of encrypted config values).
        :return: The value of the requested config key.
        """
        config_key = functools.reduce(lambda x, y: x + "." + y, config_key_as_arr)

        # This should just call get_config from repository. If None, then call get_default prob
        config = mongo.db.config.find_one({}, {config_key: 1})

        for config_key_part in config_key_as_arr:
            config = config[config_key_part]
        if should_decrypt:
            if config_key_as_arr in ENCRYPTED_CONFIG_VALUES:
                if isinstance(config, str):
                    config = get_datastore_encryptor().decrypt(config)
                elif isinstance(config, list):
                    if config:
                        if isinstance(config[0], str):
                            config = [get_datastore_encryptor().decrypt(x) for x in config]
                        elif isinstance(config[0], dict) and "public_key" in config[0]:
                            config = [decrypt_dict(SENSITIVE_SSH_KEY_FIELDS, x) for x in config]

        return config

    @staticmethod
    def set_config_value(config_key_as_arr, value):
        mongo_key = ".".join(config_key_as_arr)
        mongo.db.config.update({}, {"$set": {mongo_key: value}})

    @staticmethod
    def get_flat_config(should_decrypt=True):
        config_json = ConfigService.get_config(should_decrypt)
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

    # Not added to interface because it's doable by get_config_field + set_config_field
    @staticmethod
    def add_item_to_config_set_if_dont_exist(item_path_array, item_value, should_encrypt):
        item_key = ".".join(item_path_array)
        items_from_config = ConfigService.get_config_value(item_path_array, should_encrypt)
        if item_value in items_from_config:
            return
        if should_encrypt:
            if isinstance(item_value, dict):
                item_value = encrypt_dict(SENSITIVE_SSH_KEY_FIELDS, item_value)
            else:
                item_value = get_datastore_encryptor().encrypt(item_value)
        mongo.db.config.update({}, {"$addToSet": {item_key: item_value}})

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
    def ssh_add_keys(public_key, private_key):
        ConfigService.add_item_to_config_set_if_dont_exist(
            SSH_KEYS_PATH,
            {"public_key": public_key, "private_key": private_key},
            should_encrypt=True,
        )

    @staticmethod
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
        mongo.db.config.update({}, {"$set": config_json}, upsert=True)
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
    def init_config():
        if ConfigService.get_config(should_decrypt=False) != {}:
            return

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
                            decrypt_dict(SENSITIVE_SSH_KEY_FIELDS, config_arr[i])
                            if is_decrypt
                            else encrypt_dict(SENSITIVE_SSH_KEY_FIELDS, config_arr[i])
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
    def get_config_propagation_credentials_from_flat_config(config) -> Dict[str, List[str]]:
        return {
            "exploit_user_list": config.get("exploit_user_list", []),
            "exploit_password_list": config.get("exploit_password_list", []),
            "exploit_lm_hash_list": config.get("exploit_lm_hash_list", []),
            "exploit_ntlm_hash_list": config.get("exploit_ntlm_hash_list", []),
            "exploit_ssh_keys": config.get("exploit_ssh_keys", []),
        }
