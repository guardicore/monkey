from infection_monkey.utils.plugins.pluginTests.PluginTestClass import \
    TestPlugin


class NoInheritance:
    pass


class BadInit(TestPlugin):

    def __init__(self):
        raise Exception("TestException")


class ProperClass(TestPlugin):
    pass
