from infection_monkey.utils.plugins.pluginTests.PluginTestClass import \
    TestPlugin


class BadPluginInit(TestPlugin):

    def __init__(self):
        raise Exception("TestException")
