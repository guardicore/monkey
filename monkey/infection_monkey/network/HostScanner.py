from abc import ABCMeta, abstractmethod


class HostScanner(metaclass=ABCMeta):
    @abstractmethod
    def is_host_alive(self, host):
        raise NotImplementedError()
