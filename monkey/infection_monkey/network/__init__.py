from abc import ABCMeta, abstractmethod, abstractproperty

__author__ = 'itamar'


class HostScanner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_host_alive(self, host):
        raise NotImplementedError()


class HostFinger(object):
    __metaclass__ = ABCMeta

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


from infection_monkey.network.ping_scanner import PingScanner
from infection_monkey.network.tcp_scanner import TcpScanner
from infection_monkey.network.smbfinger import SMBFinger
from infection_monkey.network.sshfinger import SSHFinger
from infection_monkey.network.httpfinger import HTTPFinger
from infection_monkey.network.elasticfinger import ElasticFinger
from infection_monkey.network.mysqlfinger import MySQLFinger
from infection_monkey.network.info import local_ips, get_free_tcp_port
from infection_monkey.network.mssql_fingerprint import MSSQLFinger
