
from abc import ABCMeta, abstractmethod
import socket

__author__ = 'itamar'

class HostScanner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_host_alive(self, host):
        raise NotImplementedError()

class HostFinger(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_host_fingerprint(self, host):
        raise NotImplementedError()


from ping_scanner import PingScanner
from tcp_scanner import TcpScanner
from smbfinger import SMBFinger
from sshfinger import SSHFinger
from info import local_ips