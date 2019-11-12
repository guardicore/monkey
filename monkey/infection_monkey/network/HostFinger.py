from abc import abstractmethod

from infection_monkey.config import WormConfiguration
from infection_monkey.utils.plugins.plugin import Plugin


class HostFinger(Plugin):
    @staticmethod
    def base_package_file():
        import infection_monkey.network  # avoid circular imports
        return infection_monkey.network.__file__

    @staticmethod
    def base_package_name():
        import infection_monkey.network  # avoid circular imports
        return infection_monkey.network.__package__

    @property
    @abstractmethod
    def _SCANNED_SERVICE(self):
        pass

    def init_service(self, services, service_key, port):
        services[service_key] = {}
        services[service_key]['display_name'] = self._SCANNED_SERVICE
        services[service_key]['port'] = port

    @abstractmethod
    def get_host_fingerprint(self, host):
        raise NotImplementedError()

    @staticmethod
    def should_run(class_name: str) -> bool:
        return class_name in WormConfiguration.finger_classes
