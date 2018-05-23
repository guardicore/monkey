import json
import standard
import aws

ENV_DICT = {
    'standard': standard.StandardEnvironment,
    'aws': aws.AwsEnvironment
}


def load_env_from_file():
    with open('monkey_island/cc/server_config.json', 'r') as f:
        config_content = f.read()
    config_json = json.loads(config_content)
    return config_json['server_config']


try:
    __env_type = load_env_from_file()
    env = ENV_DICT[__env_type]()
except Exception:
    print('Failed initializing environment: %s' % __env_type)
    raise
