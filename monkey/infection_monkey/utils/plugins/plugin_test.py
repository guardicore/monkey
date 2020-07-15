from unittest import TestCase

from infection_monkey.utils.plugins.pluginTests.BadImport import \
    SomeDummyPlugin
from infection_monkey.utils.plugins.pluginTests.BadInit import BadPluginInit
from infection_monkey.utils.plugins.pluginTests.ComboFile import (BadInit,
                                                                  ProperClass)
from infection_monkey.utils.plugins.pluginTests.PluginTestClass import \
    TestPlugin
from infection_monkey.utils.plugins.pluginTests.PluginWorking import \
    PluginWorking


class PluginTester(TestCase):

    def test_combo_file(self):
        TestPlugin.classes_to_load = [BadInit.__name__, ProperClass.__name__]
        to_init = TestPlugin.get_classes()
        self.assertEqual(len(to_init), 2)
        objects = TestPlugin.get_instances()
        self.assertEqual(len(objects), 1)

    def test_bad_init(self):
        TestPlugin.classes_to_load = [BadPluginInit.__name__]
        to_init = TestPlugin.get_classes()
        self.assertEqual(len(to_init), 1)
        objects = TestPlugin.get_instances()
        self.assertEqual(len(objects), 0)

    def test_bad_import(self):
        TestPlugin.classes_to_load = [SomeDummyPlugin.__name__]
        to_init = TestPlugin.get_classes()
        self.assertEqual(len(to_init), 0)

    def test_flow(self):
        TestPlugin.classes_to_load = [PluginWorking.__name__]
        to_init = TestPlugin.get_classes()
        self.assertEqual(len(to_init), 1)
        objects = TestPlugin.get_instances()
        self.assertEqual(len(objects), 1)
