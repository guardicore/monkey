from infection_monkey.utils.plugins.pluginTests.PluginTestClass import PluginTester


class NoInheritance:
    pass


class BadInit(PluginTester):
    def __init__(self):
        raise Exception("TestException")


class ProperClass(PluginTester):
    pass
