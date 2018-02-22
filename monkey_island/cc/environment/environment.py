import json
import standard
import aws

ENV_DICT = {
    'standard': standard.StandardEnvironment,
    'aws': aws.AwsEnvironment
}


def load_env_from_file():
    with open('server_config.json', 'r') as f:
        config_content = f.read()
    config_json = json.loads(config_content)
    return config_json['server_config']


env = ENV_DICT[load_env_from_file()]()
