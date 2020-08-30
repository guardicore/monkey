import infection_monkey.utils.plugins.pluginTests
from infection_monkey.utils.plugins.plugin import Plugin


class TestPlugin(Plugin):
    classes_to_load = []

    @staticmethod
    def should_run(class_name):
        """
        Decides if post breach action is enabled in config
        :return: True if it needs to be ran, false otherwise
        """
        return class_name in TestPlugin.classes_to_load

    @staticmethod
    def base_package_file():
        return infection_monkey.utils.plugins.pluginTests.__file__

    @staticmethod
    def base_package_name():
        return infection_monkey.utils.plugins.pluginTests.__package__
