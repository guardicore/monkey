import logging
from typing import Dict, Mapping, Sequence

from common.agent_plugins import AgentPluginType
from common.common_consts.timeouts import CONNECTION_TIMEOUT
from common.credentials import Credentials
from common.event_queue import IAgentEventQueue
from common.types import Event
from infection_monkey import network_scanning
from infection_monkey.i_puppet import (
    ExploiterResultData,
    FingerprintData,
    IncompatibleOperatingSystemError,
    IPuppet,
    PingScanData,
    PortScanData,
)
from infection_monkey.model import TargetHost
from infection_monkey.puppet import PluginCompatabilityVerifier

from . import PluginRegistry

EMPTY_FINGERPRINT = FingerprintData(None, None, [])

logger = logging.getLogger()


class Puppet(IPuppet):
    def __init__(
        self,
        agent_event_queue: IAgentEventQueue,
        plugin_registry: PluginRegistry,
        plugin_compatability_verifier: PluginCompatabilityVerifier,
    ) -> None:
        self._plugin_registry = plugin_registry
        self._agent_event_queue = agent_event_queue
        self._plugin_compatability_verifier = plugin_compatability_verifier

    def load_plugin(self, plugin_type: AgentPluginType, plugin_name: str, plugin: object) -> None:
        self._plugin_registry.load_plugin(plugin_type, plugin_name, plugin)

    def run_credential_collector(self, name: str, options: Dict) -> Sequence[Credentials]:
        credential_collector = self._plugin_registry.get_plugin(
            AgentPluginType.CREDENTIAL_COLLECTOR, name
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
            fingerprinter = self._plugin_registry.get_plugin(AgentPluginType.FINGERPRINTER, name)
            return fingerprinter.get_host_fingerprint(host, ping_scan_data, port_scan_data, options)
        except Exception:
            logger.exception(
                f"Unhandled exception occurred " f"while trying to run {name} fingerprinter"
            )
            return EMPTY_FINGERPRINT

    def exploit_host(
        self,
        name: str,
        host: TargetHost,
        current_depth: int,
        servers: Sequence[str],
        options: Mapping,
        interrupt: Event,
    ) -> ExploiterResultData:
        if self._plugin_compatability_verifier.verify_exploiter_compatibility(name, host) is False:
            raise IncompatibleOperatingSystemError(
                f'The exploiter, "{name}", is not compatible with the operating system on {host}'
            )
        exploiter = self._plugin_registry.get_plugin(AgentPluginType.EXPLOITER, name)
        return exploiter.run(
            host=host,
            servers=servers,
            current_depth=current_depth,
            options=options,
            interrupt=interrupt,
        )

    def run_payload(self, name: str, options: Dict, interrupt: Event):
        payload = self._plugin_registry.get_plugin(AgentPluginType.PAYLOAD, name)
        payload.run(options, interrupt)

    def cleanup(self) -> None:
        pass
