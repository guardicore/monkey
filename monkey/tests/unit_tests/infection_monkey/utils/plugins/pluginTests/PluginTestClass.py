import tests.unit_tests.infection_monkey.utils.plugins.pluginTests

from infection_monkey.utils.plugins import Plugin


class PluginTester(Plugin):
    classes_to_load = []

    @staticmethod
    def should_run(class_name):
        """
        Decides if post breach action is enabled in config
        :return: True if it needs to be ran, false otherwise
        """
        return class_name in PluginTester.classes_to_load

    @staticmethod
    def base_package_file():
        return tests.unit_tests.infection_monkey.utils.plugins.pluginTests.__file__

    @staticmethod
    def base_package_name():
        return tests.unit_tests.infection_monkey.utils.plugins.pluginTests.__package__
