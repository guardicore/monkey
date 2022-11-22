import logging
import threading
from typing import Dict, Sequence

from common.common_consts.timeouts import CONNECTION_TIMEOUT
from common.credentials import Credentials
from common.event_queue import IAgentEventQueue
from common.types import PingScanData
from infection_monkey import network_scanning
from infection_monkey.i_puppet import (
    ExploiterResultData,
    FingerprintData,
    IPuppet,
    PluginType,
    PortScanData,
)
from infection_monkey.master.plugin_registry import PluginRegistry
from infection_monkey.model import VictimHost

EMPTY_FINGERPRINT = FingerprintData(None, None, [])

logger = logging.getLogger()


class Puppet(IPuppet):
    def __init__(
        self, agent_event_queue: IAgentEventQueue, plugin_registry: PluginRegistry
    ) -> None:
        self._plugin_registry = plugin_registry
        self._agent_event_queue = agent_event_queue

    def load_plugin(self, plugin_name: str, plugin: object, plugin_type: PluginType) -> None:
        self._plugin_registry.load_plugin(plugin_name, plugin, plugin_type)

    def run_credential_collector(self, name: str, options: Dict) -> Sequence[Credentials]:
        credential_collector = self._plugin_registry.get_plugin(
            name, PluginType.CREDENTIAL_COLLECTOR
        )
        return credential_collector.collect_credentials(options)

    def ping(self, host: str, timeout: float = CONNECTION_TIMEOUT) -> PingScanData:
        return network_scanning.ping(host, timeout, self._agent_event_queue)

    def scan_tcp_ports(
        self, host: str, ports: Sequence[int], timeout: float = CONNECTION_TIMEOUT
    ) -> Dict[int, PortScanData]:
        return network_scanning.scan_tcp_ports(host, ports, timeout, self._agent_event_queue)

    def fingerprint(
        self,
        name: str,
        host: str,
        ping_scan_data: PingScanData,
        port_scan_data: Dict[int, PortScanData],
        options: Dict,
    ) -> FingerprintData:
        try:
            fingerprinter = self._plugin_registry.get_plugin(name, PluginType.FINGERPRINTER)
            return fingerprinter.get_host_fingerprint(host, ping_scan_data, port_scan_data, options)
        except Exception:
            logger.exception(
                f"Unhandled exception occurred " f"while trying to run {name} fingerprinter"
            )
            return EMPTY_FINGERPRINT

    def exploit_host(
        self,
        name: str,
        host: VictimHost,
        current_depth: int,
        servers: Sequence[str],
        options: Dict,
        interrupt: threading.Event,
    ) -> ExploiterResultData:
        exploiter = self._plugin_registry.get_plugin(name, PluginType.EXPLOITER)
        return exploiter.exploit_host(host, servers, current_depth, options, interrupt)

    def run_payload(self, name: str, options: Dict, interrupt: threading.Event):
        payload = self._plugin_registry.get_plugin(name, PluginType.PAYLOAD)
        payload.run(options, interrupt)

    def cleanup(self) -> None:
        pass
