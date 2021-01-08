import pkgutil
import sys
from pathlib import PurePath
from typing import Tuple

from common.cloud.scoutsuite_consts import CloudProviders
from common.utils.exceptions import InvalidAWSKeys
from monkey_island.cc.server_utils.encryptor import encryptor
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.config_schema.config_value_paths import AWS_KEYS_PATH

_scoutsuite_api_package = pkgutil.get_loader('common.cloud.scoutsuite.ScoutSuite.__main__')


def _add_scoutsuite_to_python_path():
    scoutsuite_path = PurePath(_scoutsuite_api_package.path).parent.parent.__str__()
    sys.path.append(scoutsuite_path)


_add_scoutsuite_to_python_path()


def is_cloud_authentication_setup(provider: CloudProviders) -> Tuple[bool, str]:
    if provider == CloudProviders.AWS.value:
        if is_aws_keys_setup():
            return True, "AWS keys already setup. Run Monkey on Island to start the scan."

        import common.cloud.scoutsuite.ScoutSuite.providers.aws.authentication_strategy as auth_strategy
        try:
            profile = auth_strategy.AWSAuthenticationStrategy().authenticate()
            return True, f" Profile \"{profile.session.profile_name}\" is already setup. " \
                         f"Run Monkey on Island to start the scan."
        except Exception:
            return False, ""


def is_aws_keys_setup():
    return (ConfigService.get_config_value(AWS_KEYS_PATH + ['access_key_id']) and
            ConfigService.get_config_value(AWS_KEYS_PATH + ['secret_access_key']))


def set_aws_keys(access_key_id: str, secret_access_key: str, session_token: str):
    if not access_key_id or not secret_access_key:
        raise InvalidAWSKeys("Missing some of the following fields: access key ID, secret access key.")
    _set_aws_key('access_key_id', access_key_id)
    _set_aws_key('secret_access_key', secret_access_key)
    _set_aws_key('session_token', session_token)


def _set_aws_key(key_type: str, key_value: str):
    path_to_keys = AWS_KEYS_PATH
    encrypted_key = encryptor.enc(key_value)
    ConfigService.set_config_value(path_to_keys + [key_type], encrypted_key)


def get_aws_keys():
    return {'access_key_id': _get_aws_key('access_key_id'),
            'secret_access_key': _get_aws_key('secret_access_key'),
            'session_token': _get_aws_key('session_token')}


def _get_aws_key(key_type: str):
    path_to_keys = AWS_KEYS_PATH
    return ConfigService.get_config_value(config_key_as_arr=path_to_keys + [key_type])
