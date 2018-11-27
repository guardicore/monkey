import json
import logging
import standard
import aws

logger = logging.getLogger(__name__)

AWS = 'aws'
STANDARD = 'standard'

ENV_DICT = {
    'standard': standard.StandardEnvironment,
    'aws': aws.AwsEnvironment
}


def load_server_configuration_from_file():
    with open('monkey_island/cc/server_config.json', 'r') as f:
        config_content = f.read()
    return json.loads(config_content)


def load_env_from_file():
    config_json = load_server_configuration_from_file()
    return config_json['server_config']

try:
    __env_type = load_env_from_file()
    env = ENV_DICT[__env_type]()
    logger.info('Monkey\'s env is: {0}'.format(env.__class__.__name__))
except Exception:
    logger.error('Failed initializing environment', exc_info=True)
    raise
