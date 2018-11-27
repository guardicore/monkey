import urllib2

import cc.auth
from cc.environment import Environment

__author__ = 'itay.mizeretz'


class AwsEnvironment(Environment):
    def __init__(self):
        super(AwsEnvironment, self).__init__()
        self._instance_id = AwsEnvironment._get_instance_id()

    @staticmethod
    def _get_instance_id():
        return urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read()

    @staticmethod
    def _get_region():
        return urllib2.urlopen('http://169.254.169.254/latest/meta-data/placement/availability-zone').read()[:-1]

    def is_auth_enabled(self):
        return True

    def get_auth_users(self):
        return [
            cc.auth.User(1, 'monkey', self._instance_id)
        ]
