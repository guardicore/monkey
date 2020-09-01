from common.cloud.aws.aws_instance import AwsInstance
from monkey_island.cc.environment import Environment

__author__ = 'itay.mizeretz'


class AwsEnvironment(Environment):

    _credentials_required = True

    def __init__(self, config):
        super(AwsEnvironment, self).__init__(config)
        # Not suppressing error here on purpose. This is critical if we're on AWS env.
        self.aws_info = AwsInstance()
        self._instance_id = self._get_instance_id()
        self.region = self._get_region()

    def _get_instance_id(self):
        return self.aws_info.get_instance_id()

    def _get_region(self):
        return self.aws_info.get_region()

    def get_auth_users(self):
        if self._is_registered():
            return self._config.get_users()
        else:
            return []
