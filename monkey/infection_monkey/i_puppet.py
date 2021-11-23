import abc
import threading
from collections import namedtuple
from enum import Enum
from typing import Dict, Optional, Tuple


class PortStatus(Enum):
    OPEN = 1
    CLOSED = 2


PortScanData = namedtuple("PortScanData", ["port", "status", "banner", "service"])


class IPuppet(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run_sys_info_collector(self, name: str) -> Dict:
        """
        Runs a system info collector
        :param str name: The name of the system info collector to run
        :return: A dictionary containing the information collected from the system
        :rtype: Dict
        """

    @abc.abstractmethod
    def run_pba(self, name: str, options: Dict) -> None:
        """
        Runs a post-breach action (PBA)
        :param str name: The name of the post-breach action to run
        :param Dict options: A dictionary containing options that modify the behavior of the PBA
        """

    @abc.abstractmethod
    def ping(self, host: str) -> Tuple[bool, Optional[str]]:
        """
        Sends a ping (ICMP packet) to a remote host
        :param str host: The domain name or IP address of a host
        :return: A tuple that contains whether or not the host responded and the host's inferred
                 operating system
        :rtype: Tuple[bool, Optional[str]]
        """

    @abc.abstractmethod
    def scan_tcp_port(self, host: str, port: int) -> PortScanData:
        """
        Scans a TCP port on a remote host
        :param str host: The domain name or IP address of a host
        :param int port: A TCP port number to scan
        :return: The data collected by scanning the provided host:port combination
        :rtype: PortScanData
        """

    @abc.abstractmethod
    def fingerprint(self, name: str, host: str) -> Dict:
        """
        Runs a fingerprinter against a remote host
        :param str name: The name of the fingerprinter to run
        :param str host: The domain name or IP address of a host
        :return: A dictionary containing the information collected by the fingerprinter
        :rtype: Dict
        """

    @abc.abstractmethod
    def exploit_host(self, name: str, host: str, options: Dict, interrupt: threading.Event) -> bool:
        """
        Runs an exploiter against a remote host
        :param str name: The name of the exploiter to run
        :param str host: The domain name or IP address of a host
        :param Dict options: A dictionary containing options that modify the behavior of the
                             exploiter
        :return: True if exploitation was successful, False otherwise
        :rtype: bool
        """

    @abc.abstractmethod
    def run_payload(self, name: str, options: Dict, interrupt: threading.Event) -> None:
        """
        Runs a payload
        :param str name: The name of the payload to run
        :param Dict options: A dictionary containing options that modify the behavior of the payload
        """

    @abc.abstractmethod
    def cleanup(self) -> None:
        """
        Revert any changes made to the system by the puppet.
        """
