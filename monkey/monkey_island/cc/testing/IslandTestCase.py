import unittest

import mongoengine

import monkey_island.cc.environment.environment_singleton as env_singleton
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.edge import Edge
from monkey_island.cc.models.zero_trust.finding import Finding


class IslandTestCase(unittest.TestCase):

    def __init__(self, methodName):
        # Make sure test is working with mongomock
        if mongoengine.connection.get_connection().server_info()['sysInfo'] != 'Mock':
            mongoengine.disconnect()
            mongoengine.connect('mongoenginetest', host='mongomock://localhost')
        else:
            IslandTestCase.clean_db()
        super().__init__(methodName)

    def fail_if_not_testing_env(self):
        self.assertFalse(not env_singleton.env.testing, "Change server_config.json to testing environment.")

    @staticmethod
    def clean_db():
        IslandTestCase._clean_edge_db()
        IslandTestCase._clean_monkey_db()
        IslandTestCase._clean_finding_db()

    @staticmethod
    def _clean_monkey_db():
        Monkey.objects().delete()

    @staticmethod
    def _clean_edge_db():
        Edge.objects().delete()

    @staticmethod
    def _clean_finding_db():
        Finding.objects().delete()
