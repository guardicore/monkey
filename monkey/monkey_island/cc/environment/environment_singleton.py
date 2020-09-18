import logging

import monkey_island.cc.resources.auth.user_store as user_store
from monkey_island.cc.environment import (EnvironmentConfig, aws, password,
                                          standard, testing)

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

env = None


def set_env(env_type: str, env_config: EnvironmentConfig):
    global env
    if env_type in ENV_DICT:
        env = ENV_DICT[env_type](env_config)


def set_to_standard():
    global env
    if env:
        env_config = env.get_config()
        env_config.server_config = 'standard'
        set_env('standard', env_config)
        env.save_config()
        user_store.UserStore.set_users(env.get_auth_users())


try:
    config = EnvironmentConfig.get_from_file()
    __env_type = config.server_config
    set_env(__env_type, config)
    # noinspection PyUnresolvedReferences
    logger.info('Monkey\'s env is: {0}'.format(env.__class__.__name__))
except Exception:
    logger.error('Failed initializing environment', exc_info=True)
    raise
