from config import WormConfiguration
from infection_monkey.utils.plugins.plugin import Plugin


import infection_monkey.system_info.collectors


class SystemInfoCollector(Plugin):
    def __init__(self, name="unknown"):
        self.name = name

    @staticmethod
    def should_run(class_name) -> bool:
        return class_name in WormConfiguration.system_info_collectors

    @staticmethod
    def base_package_file():
        return infection_monkey.system_info.collectors.__file__

    @staticmethod
    def base_package_name():
        return infection_monkey.system_info.collectors.__package__

    def collect(self) -> dict:
        """
        Collect the relevant information and return it in a dictionary.
        To be implemented by each collector.
        TODO should this be an abstractmethod, or will that ruin the plugin system somehow? if can be abstract should add UT
        """
        raise NotImplementedError()
