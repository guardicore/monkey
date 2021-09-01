import logging

from monkey_island.cc.environment import EnvironmentConfig, aws, password

logger = logging.getLogger(__name__)

AWS = "aws"
PASSWORD = "password"

ENV_DICT = {
    AWS: aws.AwsEnvironment,
    PASSWORD: password.PasswordEnvironment,
}

env = None


def set_env(env_type: str, env_config: EnvironmentConfig):
    global env
    if env_type in ENV_DICT:
        env = ENV_DICT[env_type](env_config)


def initialize_from_file(file_path):
    try:
        config = EnvironmentConfig(file_path)

        __env_type = config.server_config
        set_env(__env_type, config)
        # noinspection PyUnresolvedReferences
        logger.info("Monkey's env is: {0}".format(env.__class__.__name__))
    except Exception:
        logger.error("Failed initializing environment", exc_info=True)
        raise
