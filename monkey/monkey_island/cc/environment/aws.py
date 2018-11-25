import cc.auth
from cc.environment import Environment
from common.cloud.aws import Aws

__author__ = 'itay.mizeretz'


class AwsEnvironment(Environment):
    def __init__(self):
        super(AwsEnvironment, self).__init__()
        self._instance_id = AwsEnvironment._get_instance_id()

    @staticmethod
    def _get_instance_id():
        return Aws.get_instance_id()

    def is_auth_enabled(self):
        return True

    def get_auth_users(self):
        return [
            cc.auth.User(1, 'monkey', self._instance_id)
        ]
