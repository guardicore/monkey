from tests.unit_tests.infection_monkey.utils.plugins.pluginTests.PluginTestClass import PluginTester


class BadPluginInit(PluginTester):
    def __init__(self):
        raise Exception("TestException")
