# test - should run true
# test - should run false
# test - invalid parent class but should run true
# test - imported from other file, should not collect
# test - failed to instance


from unittest import TestCase
import infection_monkey.utils.plugins.plugins_testcases
from infection_monkey.utils.plugins.load_plugins import get_instances
from infection_monkey.utils.plugins.plugin import Plugin


class PluginTester(TestCase):

    def setUp(self):
        pass

    def test_plugins(self):
        res = get_instances(infection_monkey.utils.plugins.plugins_testcases.__package__,infection_monkey.utils.plugins.plugins_testcases.__file__,Plugin)
        self.assertEqual(len(res), 1)
