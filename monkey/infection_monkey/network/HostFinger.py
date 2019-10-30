from abc import ABCMeta, abstractproperty, abstractmethod

from infection_monkey.config import WormConfiguration


class HostFinger(object, metaclass=ABCMeta):
    @abstractproperty
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
    def should_run(class_name):
        """
        Decides if post breach action is enabled in config
        :return: True if it needs to be ran, false otherwise
        """
        return class_name in WormConfiguration.finger_classes
