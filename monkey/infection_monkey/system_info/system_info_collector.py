from abc import ABCMeta, abstractmethod

import infection_monkey.system_info.collectors
from infection_monkey.config import WormConfiguration
from infection_monkey.utils.plugins.plugin import Plugin


class SystemInfoCollector(Plugin, metaclass=ABCMeta):
    """
    ABC for system info collection. See system_info_collector_handler for more info. Basically, to implement a new system info
    collector, inherit from this class in an implementation in the infection_monkey.system_info.collectors class, and override
    the 'collect' method. Don't forget to parse your results in the Monkey Island and to add the collector to the configuration
    as well - see monkey_island.cc.services.processing.system_info_collectors for examples.

    See the Wiki page "How to add a new System Info Collector to the Monkey?" for a detailed guide.
    """
    def __init__(self, name="unknown"):
        self.name = name

    @staticmethod
    def should_run(class_name) -> bool:
        return class_name in WormConfiguration.system_info_collector_classes

    @staticmethod
    def base_package_file():
        return infection_monkey.system_info.collectors.__file__

    @staticmethod
    def base_package_name():
        return infection_monkey.system_info.collectors.__package__

    @abstractmethod
    def collect(self) -> dict:
        """
        Collect the relevant information and return it in a dictionary.
        To be implemented by each collector.
        """
        raise NotImplementedError()
