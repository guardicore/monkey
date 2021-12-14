import abc
import threading
from collections import namedtuple
from enum import Enum
from typing import Dict, Tuple

from infection_monkey.puppet.plugin_type import PluginType


class PortStatus(Enum):
    OPEN = 1
    CLOSED = 2


class UnknownPluginError(Exception):
    pass


ExploiterResultData = namedtuple("ExploiterResultData", ["success", "info", "attempts"])
PingScanData = namedtuple("PingScanData", ["response_received", "os"])
PortScanData = namedtuple("PortScanData", ["port", "status", "banner", "service"])
FingerprintData = namedtuple("FingerprintData", ["os_type", "os_version", "services"])
PostBreachData = namedtuple("PostBreachData", ["command", "result"])


class IPuppet(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load_plugin(self, plugin: object, plugin_type: PluginType) -> None:
        """
        Loads a plugin into the puppet.
        :param object plugin: The plugin object to load
        :param PluginType plugin_type: The type of plugin being loaded
        """

    @abc.abstractmethod
    def run_sys_info_collector(self, name: str) -> Dict:
        """
        Runs a system info collector
        :param str name: The name of the system info collector to run
        :return: A dictionary containing the information collected from the system
        :rtype: Dict
        """

    @abc.abstractmethod
    def run_pba(self, name: str, options: Dict) -> PostBreachData:
        """
        Runs a post-breach action (PBA)
        :param str name: The name of the post-breach action to run
        :param Dict options: A dictionary containing options that modify the behavior of the PBA
        :rtype: PostBreachData
        """

    @abc.abstractmethod
    def ping(self, host: str, timeout: float) -> PingScanData:
        """
        Sends a ping (ICMP packet) to a remote host
        :param str host: The domain name or IP address of a host
        :param float timeout: The maximum amount of time (in seconds) to wait for a response
        :return: The data collected by attempting to ping the target host
        :rtype: PingScanData
        """

    @abc.abstractmethod
    def scan_tcp_port(self, host: str, port: int, timeout: float) -> PortScanData:
        """
        Scans a TCP port on a remote host
        :param str host: The domain name or IP address of a host
        :param int port: A TCP port number to scan
        :param float timeout: The maximum amount of time (in seconds) to wait for a response
        :return: The data collected by scanning the provided host:port combination
        :rtype: PortScanData
        """

    @abc.abstractmethod
    def fingerprint(
        self,
        name: str,
        host: str,
        ping_scan_data: PingScanData,
        port_scan_data: Dict[int, PortScanData],
    ) -> FingerprintData:
        """
        Runs a fingerprinter against a remote host
        :param str name: The name of the fingerprinter to run
        :param str host: The domain name or IP address of a host
        :param PingScanData ping_scan_data: Data retrieved from the target host via ICMP
        :param Dict[int, PortScanData] port_scan_data: Data retrieved from the target host via a TCP
                                                       port scan
        :return: The data collected by running the fingerprinter on the specified host
        :rtype: FingerprintData
        """

    @abc.abstractmethod
    def exploit_host(
        self, name: str, host: str, options: Dict, interrupt: threading.Event
    ) -> ExploiterResultData:
        """
        Runs an exploiter against a remote host
        :param str name: The name of the exploiter to run
        :param str host: The domain name or IP address of a host
        :param Dict options: A dictionary containing options that modify the behavior of the
                             exploiter
        :return: True if exploitation was successful, False otherwise
        :rtype: ExploiterResultData
        """

    @abc.abstractmethod
    def run_payload(
        self, name: str, options: Dict, interrupt: threading.Event
    ) -> Tuple[None, bool, str]:
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
