from abc import abstractmethod

import infection_monkey.payload
from infection_monkey.utils.plugins.plugin import Plugin


class Payload(Plugin):
    @staticmethod
    def base_package_file():
        return infection_monkey.payload.__file__

    @staticmethod
    def base_package_name():
        return infection_monkey.payload.__package__

    @abstractmethod
    def run_payload(self):
        raise NotImplementedError()

    def should_run(self):
        pass
