import logging
import threading
from typing import Dict

from infection_monkey import network
from infection_monkey.i_puppet import (
    ExploiterResultData,
    FingerprintData,
    IPuppet,
    PingScanData,
    PluginType,
    PortScanData,
    PostBreachData,
)

from .mock_puppet import MockPuppet
from .plugin_registry import PluginRegistry

logger = logging.getLogger()


class Puppet(IPuppet):
    def __init__(self) -> None:
        self._mock_puppet = MockPuppet()
        self._plugin_registry = PluginRegistry()

    def load_plugin(self, plugin_name: str, plugin: object, plugin_type: PluginType) -> None:
        self._plugin_registry.load_plugin(plugin_name, plugin, plugin_type)

    def run_sys_info_collector(self, name: str) -> Dict:
        return self._mock_puppet.run_sys_info_collector(name)

    def run_pba(self, name: str, options: Dict) -> PostBreachData:
        return self._mock_puppet.run_pba(name, options)

    def ping(self, host: str, timeout: float = 1) -> PingScanData:
        return network.ping(host, timeout)

    def scan_tcp_port(self, host: str, port: int, timeout: float = 3) -> PortScanData:
        return self._mock_puppet.scan_tcp_port(host, port, timeout)

    def fingerprint(
        self,
        name: str,
        host: str,
        ping_scan_data: PingScanData,
        port_scan_data: Dict[int, PortScanData],
    ) -> FingerprintData:
        return self._mock_puppet.fingerprint(name, host, ping_scan_data, port_scan_data)

    def exploit_host(
        self, name: str, host: str, options: Dict, interrupt: threading.Event
    ) -> ExploiterResultData:
        return self._mock_puppet.exploit_host(name, host, options, interrupt)

    def run_payload(self, name: str, options: Dict, interrupt: threading.Event):
        payload = self._plugin_registry.get_plugin(name, PluginType.PAYLOAD)
        payload.run(options, interrupt)

    def cleanup(self) -> None:
        pass
