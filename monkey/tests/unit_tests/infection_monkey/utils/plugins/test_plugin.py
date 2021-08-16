from unittest import TestCase

from tests.unit_tests.infection_monkey.utils.plugins.pluginTests.BadImport import SomeDummyPlugin
from tests.unit_tests.infection_monkey.utils.plugins.pluginTests.BadInit import BadPluginInit
from tests.unit_tests.infection_monkey.utils.plugins.pluginTests.ComboFile import (
    BadInit,
    ProperClass,
)
from tests.unit_tests.infection_monkey.utils.plugins.pluginTests.PluginTestClass import PluginTester
from tests.unit_tests.infection_monkey.utils.plugins.pluginTests.PluginWorking import PluginWorking


class TestPlugin(TestCase):
    def test_combo_file(self):
        PluginTester.classes_to_load = [BadInit.__name__, ProperClass.__name__]
        to_init = PluginTester.get_classes()
        self.assertEqual(len(to_init), 2)
        objects = PluginTester.get_instances()
        self.assertEqual(len(objects), 1)

    def test_bad_init(self):
        PluginTester.classes_to_load = [BadPluginInit.__name__]
        to_init = PluginTester.get_classes()
        self.assertEqual(len(to_init), 1)
        objects = PluginTester.get_instances()
        self.assertEqual(len(objects), 0)

    def test_bad_import(self):
        PluginTester.classes_to_load = [SomeDummyPlugin.__name__]
        to_init = PluginTester.get_classes()
        self.assertEqual(len(to_init), 0)

    def test_flow(self):
        PluginTester.classes_to_load = [PluginWorking.__name__]
        to_init = PluginTester.get_classes()
        self.assertEqual(len(to_init), 1)
        objects = PluginTester.get_instances()
        self.assertEqual(len(objects), 1)
