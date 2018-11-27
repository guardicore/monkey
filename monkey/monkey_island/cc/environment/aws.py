import cc.auth
from cc.environment import Environment
from common.cloud.aws import AWS

__author__ = 'itay.mizeretz'


class AwsEnvironment(Environment):
    def __init__(self):
        super(AwsEnvironment, self).__init__()
        self.aws_info = AWS()
        self._instance_id = self._get_instance_id()
        self.region = self._get_region()

    def _get_instance_id(self):
        return self.aws_info.get_instance_id()

    def _get_region(self):
        return self.aws_info.get_region()

    @staticmethod
    def _get_region():
        return urllib2.urlopen('http://169.254.169.254/latest/meta-data/placement/availability-zone').read()[:-1]

    def is_auth_enabled(self):
        return True

    def get_auth_users(self):
        return [
            cc.auth.User(1, 'monkey', self._instance_id)
        ]
