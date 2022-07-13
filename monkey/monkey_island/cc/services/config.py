import collections
import functools
import logging

from common.config_value_paths import (
    LM_HASH_LIST_PATH,
    NTLM_HASH_LIST_PATH,
    PASSWORD_LIST_PATH,
    PBA_LINUX_FILENAME_PATH,
    PBA_WINDOWS_FILENAME_PATH,
    SSH_KEYS_PATH,
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
