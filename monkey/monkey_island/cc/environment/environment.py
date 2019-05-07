import json
import logging
import os

env = None

from monkey_island.cc.environment import standard
from monkey_island.cc.environment import testing
from monkey_island.cc.environment import aws
from monkey_island.cc.environment import password
from monkey_island.cc.consts import MONKEY_ISLAND_ABS_PATH

__author__ = 'itay.mizeretz'

logger = logging.getLogger(__name__)

AWS = 'aws'
STANDARD = 'standard'
PASSWORD = 'password'
TESTING = 'testing'

ENV_DICT = {
    STANDARD: standard.StandardEnvironment,
    AWS: aws.AwsEnvironment,
    PASSWORD: password.PasswordEnvironment,
    TESTING: testing.TestingEnvironment
}


def load_server_configuration_from_file():
    with open(os.path.join(MONKEY_ISLAND_ABS_PATH, 'cc/server_config.json'), 'r') as f:
        config_content = f.read()
    return json.loads(config_content)


def load_env_from_file():
    config_json = load_server_configuration_from_file()
    return config_json['server_config']


try:
    config_json = load_server_configuration_from_file()
    __env_type = config_json['server_config']
    env = ENV_DICT[__env_type]()
    env.set_config(config_json)
    logger.info('Monkey\'s env is: {0}'.format(env.__class__.__name__))
except Exception:
    logger.error('Failed initializing environment', exc_info=True)
    raise
