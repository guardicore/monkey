import monkey_island.cc.auth
from monkey_island.cc.environment import Environment
from common.cloud.aws_instance import AwsInstance
from Crypto.Hash import SHA3_512

__author__ = 'itay.mizeretz'


class AwsEnvironment(Environment):
    def __init__(self):
        super(AwsEnvironment, self).__init__()
        self.aws_info = AwsInstance()
        self._instance_id = self._get_instance_id()
        self.region = self._get_region()

    def _get_instance_id(self):
        return self.aws_info.get_instance_id()

    def _get_region(self):
        return self.aws_info.get_region()

    def get_auth_users(self):
        return [
            monkey_island.cc.auth.User(1, 'monkey', self.hash_secret(self._instance_id))
        ]
