import unittest
from monkey_island.cc.environment.environment import env
from monkey_island.cc.models import Monkey


class IslandTestCase(unittest.TestCase):
    def fail_if_not_testing_env(self):
        self.failIf(not env.testing, "Change server_config.json to testing environment.")

    @staticmethod
    def clean_monkey_db():
        Monkey.objects().delete()
