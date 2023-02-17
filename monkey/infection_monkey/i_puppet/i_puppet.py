import abc
from collections import namedtuple
from dataclasses import dataclass
from typing import Dict, Mapping, Optional, Sequence

from common.agent_plugins import AgentPluginType
from common.credentials import Credentials
from common.types import Event, NetworkPort
from infection_monkey.i_puppet.target_host import TargetHost

from . import PingScanData, PortScanData


class UnknownPluginError(Exception):
    pass


class RejectedRequestError(Exception):
    pass


class IncompatibleOperatingSystemError(RejectedRequestError):
    pass


@dataclass
class ExploiterResultData:
    exploitation_success: bool = False
    propagation_success: bool = False
    os: str = ""
    info: Optional[Mapping] = None
    error_message: str = ""


FingerprintData = namedtuple("FingerprintData", ["os_type", "os_version", "services"])


class IPuppet(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load_plugin(self, plugin_type: AgentPluginType, plugin_name: str, plugin: object) -> None:
        """
        Loads a plugin into the puppet

        :param AgentPluginType plugin_type: The type of plugin being loaded
        :param str plugin_name: The plugin class name
        :param object plugin: The plugin object to load
        """

    @abc.abstractmethod
    def run_credential_collector(self, name: str, options: Dict) -> Sequence[Credentials]:
        """
        Runs a credential collector

        :param str name: The name of the credential collector to run
        :param Dict options: A dictionary containing options that modify the behavior of the
                             Credential collector
        :return: A sequence of Credentials that have been collected from the system
        :rtype: Sequence[Credentials]
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
    def scan_tcp_ports(
        self, host: str, ports: Sequence[NetworkPort], timeout: float = 3
    ) -> Dict[NetworkPort, PortScanData]:
        """
        Scans a list of TCP ports on a remote host

        :param host: The domain name or IP address of a host
        :param ports: List of TCP port numbers to scan
        :param timeout: The maximum amount of time (in seconds) to wait for a response
        :return: The data collected by scanning the provided host:ports combination
        """

    @abc.abstractmethod
    def fingerprint(
        self,
        name: str,
        host: str,
        ping_scan_data: PingScanData,
        port_scan_data: Dict[NetworkPort, PortScanData],
        options: Dict,
    ) -> FingerprintData:
        """
        Runs a specific fingerprinter to attempt to gather detailed information about a host and its
        services

        :param name: The name of the fingerprinter to run
        :param host: The domain name or IP address of a host
        :param ping_scan_data: Data retrieved from the target host via ICMP
        :param port_scan_data: Data retrieved from the target host via a TCP
                                                       port scan
        :param options: A dictionary containing options that modify the behavior of the
                        fingerprinter
        :return: Detailed information about the target host
        """

    @abc.abstractmethod
    def exploit_host(
        self,
        name: str,
        host: TargetHost,
        current_depth: int,
        servers: Sequence[str],
        options: Mapping,
        interrupt: Event,
    ) -> ExploiterResultData:
        """
        Runs an exploiter against a remote host

        :param str name: The name of the exploiter to run
        :param TargetHost host: A TargetHost object representing the target to exploit
        :param int current_depth: The current propagation depth
        :param servers: List of socket addresses for victim to connect back to
        :param Dict options: A dictionary containing options that modify the behavior of the
                             exploiter
        :param Event interrupt: An `Event` object that signals the exploit to stop
                                          executing and clean itself up.
        :raises IncompatibleOperatingSystemError: If an exploiter is not compatible with the target
                                                  host's operating system
        :return: True if exploitation was successful, False otherwise
        :rtype: ExploiterResultData
        """

    @abc.abstractmethod
    def run_payload(self, name: str, options: Dict, interrupt: Event):
        """
        Runs a payload

        :param str name: The name of the payload to run
        :param Dict options: A dictionary containing options that modify the behavior of the payload
        :param Event interrupt: An `Event` object that signals the payload to stop
                                          executing and clean itself up.
        """

    @abc.abstractmethod
    def cleanup(self) -> None:
        """
        Revert any changes made to the system by the puppet.
        """
