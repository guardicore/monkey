import json
import logging

env = None

from monkey_island.cc.environment import standard, EnvironmentConfig
from monkey_island.cc.environment import testing
from monkey_island.cc.environment import aws
from monkey_island.cc.environment import password

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

try:
    config = EnvironmentConfig.get_from_file()
    __env_type = config.server_config
    env = ENV_DICT[__env_type]()
    env.set_config(config)
    logger.info('Monkey\'s env is: {0}'.format(env.__class__.__name__))
except Exception:
    logger.error('Failed initializing environment', exc_info=True)
    raise
