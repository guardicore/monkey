from abc import ABCMeta, abstractmethod
from infection_monkey.utils import get_current_time_string

__author__ = 'itamar'


class HostScanner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_host_alive(self, host):
        raise NotImplementedError()


class HostFinger(object):
    __metaclass__ = ABCMeta

    _SCANNED_SERVICE = ''

    def format_service_info(self, port=None, url=None):
        if port:
            service_endpoint = port
        elif url:
            service_endpoint = url
        else:
            raise NotImplementedError("You must pass either port or url to get formatted service info.")
        if not self._SCANNED_SERVICE:
            raise NotImplementedError("You must override _SCANNED_SERVICE property"
                                      " to name what service is being scanned.")
        return {'display_name': self._SCANNED_SERVICE,
                'endpoint': service_endpoint,
                'time': get_current_time_string()}

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
