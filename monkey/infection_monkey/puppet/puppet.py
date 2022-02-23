import logging
import threading
from typing import Dict, List, Sequence

from infection_monkey import network
from infection_monkey.i_puppet import (
    Credentials,
    ExploiterResultData,
    FingerprintData,
    IPuppet,
    PingScanData,
    PluginType,
    PortScanData,
    PostBreachData,
)

from ..telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from .mock_puppet import MockPuppet
from .plugin_registry import PluginRegistry

logger = logging.getLogger()


class Puppet(IPuppet):
    def __init__(self, telemetry_messenger: ITelemetryMessenger) -> None:
        self._mock_puppet = MockPuppet()
        self._plugin_registry = PluginRegistry()
        self._telemetry_messenger = telemetry_messenger

    def load_plugin(self, plugin_name: str, plugin: object, plugin_type: PluginType) -> None:
        self._plugin_registry.load_plugin(plugin_name, plugin, plugin_type)

    def run_credential_collector(self, name: str, options: Dict) -> Sequence[Credentials]:
        credential_collector = self._plugin_registry.get_plugin(
            name, PluginType.CREDENTIAL_COLLECTOR
        )
        return credential_collector.collect_credentials(options)

    def run_pba(self, name: str, options: Dict) -> PostBreachData:
        return self._mock_puppet.run_pba(name, options)

    def ping(self, host: str, timeout: float = 1) -> PingScanData:
        return network.ping(host, timeout)

    def scan_tcp_ports(
        self, host: str, ports: List[int], timeout: float = 3
    ) -> Dict[int, PortScanData]:
        return network.scan_tcp_ports(host, ports, timeout)

    def fingerprint(
        self,
        name: str,
        host: str,
        ping_scan_data: PingScanData,
        port_scan_data: Dict[int, PortScanData],
        options: Dict,
    ) -> FingerprintData:
        fingerprinter = self._plugin_registry.get_plugin(name, PluginType.FINGERPRINTER)
        return fingerprinter.get_host_fingerprint(host, ping_scan_data, port_scan_data, options)

    # TODO: host should be VictimHost, at the moment it can't because of circular dependency
    def exploit_host(
        self, name: str, host: object, options: Dict, interrupt: threading.Event
    ) -> ExploiterResultData:
        exploiter = self._plugin_registry.get_plugin(name, PluginType.EXPLOITER)
        return exploiter.exploit_host(host, self._telemetry_messenger, options)

    def run_payload(self, name: str, options: Dict, interrupt: threading.Event):
        payload = self._plugin_registry.get_plugin(name, PluginType.PAYLOAD)
        payload.run(options, interrupt)

    def cleanup(self) -> None:
        pass
