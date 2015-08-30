
from abc import ABCMeta, abstractmethod

__author__ = 'itamar'

class HostScanner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_host_alive(self, host):
        raise NotImplementedError()


from ping_scanner import PingScanner
from tcp_scanner import TcpScanner