import logging
import threading
from typing import Dict

from infection_monkey.i_puppet import (
    ExploiterResultData,
    FingerprintData,
    IPuppet,
    PingScanData,
    PortScanData,
    PostBreachData,
)
from infection_monkey.puppet.plugin_type import PluginType

logger = logging.getLogger()


class Puppet(IPuppet):
    def load_plugin(self, plugin: object, plugin_type: PluginType) -> None:
        pass

    def run_sys_info_collector(self, name: str) -> Dict:
        pass

    def run_pba(self, name: str, options: Dict) -> PostBreachData:
        pass

    def ping(self, host: str, timeout: float = 1) -> PingScanData:
        pass

    def scan_tcp_port(self, host: str, port: int, timeout: float = 3) -> PortScanData:
        pass

    def fingerprint(
        self,
        name: str,
        host: str,
        ping_scan_data: PingScanData,
        port_scan_data: Dict[int, PortScanData],
    ) -> FingerprintData:
        pass

    def exploit_host(
        self, name: str, host: str, options: Dict, interrupt: threading.Event
    ) -> ExploiterResultData:
        pass

    def run_payload(self, name: str, options: Dict, interrupt: threading.Event):
        pass

    def cleanup(self) -> None:
        pass
