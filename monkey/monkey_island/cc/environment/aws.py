from common.cloud.aws.aws_instance import AwsInstance
from monkey_island.cc.environment import Environment


class AwsEnvironment(Environment):
    _credentials_required = True

    def __init__(self, config):
        super(AwsEnvironment, self).__init__(config)
        # Not suppressing error here on purpose. This is critical if we're on AWS env.
        self.aws_info = AwsInstance()

    def get_auth_users(self):
        if self._is_registered():
            return [self._config.get_user()]
        else:
            return []
