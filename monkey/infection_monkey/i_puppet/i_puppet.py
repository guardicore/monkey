import abc
from typing import Any, Dict, Mapping, Sequence

from agentpluginapi import (
    ExploiterResult,
    FingerprintData,
    PingScanData,
    PortScanDataDict,
    TargetHost,
)
from monkeytypes import AgentPluginType, Credentials, Event, NetworkPort


class UnknownPluginError(Exception):
    pass


class RejectedRequestError(Exception):
    pass


class IncompatibleLocalOperatingSystemError(RejectedRequestError):
    """Raised when a plugin is not compatible with the local machines's OS"""


class IncompatibleTargetOperatingSystemError(RejectedRequestError):
    """Raised when a plugin is not compatible with the target machines's OS"""


class IPuppet(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load_plugin(self, plugin_type: AgentPluginType, plugin_name: str, plugin: object) -> None:
        """
        Loads a plugin into the puppet

        :param plugin_type: The type of plugin being loaded
        :param plugin_name: The plugin class name
        :param plugin: The plugin object to load
        """

    @abc.abstractmethod
    def run_credentials_collector(
        self, name: str, options: Mapping[str, Any], interrupt: Event
    ) -> Sequence[Credentials]:
        """
        Runs a credentials collector

        :param name: The name of the credentials collector to run
        :param options: A dictionary containing options that modify the behavior of the
                        Credentials collector
        :param interrupt: An event that can be used to interrupt the credentials collector
        :return: A sequence of Credentials that have been collected from the system
        """

    @abc.abstractmethod
    def ping(self, host: str, timeout: float) -> PingScanData:
        """
        Sends a ping (ICMP packet) to a remote host

        :param host: The domain name or IP address of a host
        :param timeout: The maximum amount of time (in seconds) to wait for a response
        :return: The data collected by attempting to ping the target host
        """

    @abc.abstractmethod
    def scan_tcp_ports(
        self, host: str, ports: Sequence[NetworkPort], timeout: float = 3
    ) -> PortScanDataDict:
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
        port_scan_data: PortScanDataDict,
        options: Dict,
    ) -> FingerprintData:
        """
        Runs a specific fingerprinter to attempt to gather detailed information about a host and its
        services

        :param name: The name of the fingerprinter to run
        :param host: The domain name or IP address of a host
        :param ping_scan_data: Data retrieved from the target host via ICMP
        :param port_scan_data: Data retrieved from the target host via a TCP port scan
        :param options: A dictionary containing options that modify the behavior of the
                        fingerprinter
        :return: Detailed information about the target host
        """

    @abc.abstractmethod
    def exploit_host(
        self,
        name: str,
        host: TargetHost,
        options: Mapping,
        interrupt: Event,
    ) -> ExploiterResult:
        """
        Runs an exploiter against a remote host

        :param name: The name of the exploiter to run
        :param host: A TargetHost object representing the target to exploit
        :param options: A dictionary containing options that modify the behavior of the exploiter
        :param interrupt: An `Event` object that signals the exploit to stop executing and clean
                          itself up.
        :raises IncompatibleLocalOperatingSystemError: If an exploiter plugin is not compatible with
                                                       the local host's operating system
        :raises IncompatibleTargetOperatingSystemError: If an exploiter is not compatible with the
                                                        target host's operating system
        :return: The result of the exploit attempt
        """

    @abc.abstractmethod
    def run_payload(self, name: str, options: Dict, interrupt: Event):
        """
        Runs a payload

        :param name: The name of the payload to run
        :param options: A dictionary containing options that modify the behavior of the payload
        :param interrupt: An `Event` object that signals the payload to stop executing and clean
                          itself up.
        """

    @abc.abstractmethod
    def cleanup(self) -> None:
        """
        Revert any changes made to the system by the puppet.
        """
