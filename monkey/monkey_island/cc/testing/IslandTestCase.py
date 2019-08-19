import unittest
from monkey_island.cc.environment.environment import env
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.zero_trust.finding import Finding


class IslandTestCase(unittest.TestCase):
    def fail_if_not_testing_env(self):
        self.failIf(not env.testing, "Change server_config.json to testing environment.")

    @staticmethod
    def clean_monkey_db():
        Monkey.objects().delete()

    @staticmethod
    def clean_finding_db():
        Finding.objects().delete()
