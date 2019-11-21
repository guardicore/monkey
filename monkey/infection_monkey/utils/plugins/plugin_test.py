from unittest import TestCase

from infection_monkey.utils.plugins.pluginTests.PluginWorking import pluginWorking
from infection_monkey.utils.plugins.pluginTests.BadImport import SomeDummyPlugin
from infection_monkey.utils.plugins.pluginTests.BadInit import badPluginInit
from infection_monkey.utils.plugins.pluginTests.PluginTestClass import TestPlugin


class PluginTester(TestCase):

    def setUp(self):
        pass

    def test_bad_init(self):
        TestPlugin.classes_to_load = [badPluginInit.__name__]
        to_init = TestPlugin.get_classes()
        self.assertEqual(len(to_init), 1)
        objects = TestPlugin.get_instances()
        self.assertEqual(len(objects), 0)

    def test_bad_import(self):
        TestPlugin.classes_to_load = [SomeDummyPlugin.__name__]
        to_init = TestPlugin.get_classes()
        self.assertEqual(len(to_init), 0)

    def test_flow(self):
        TestPlugin.classes_to_load = [pluginWorking.__name__]
        to_init = TestPlugin.get_classes()
        self.assertEqual(len(to_init), 1)
        objects = TestPlugin.get_instances()
        self.assertEqual(len(objects), 1)
