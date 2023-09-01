import re
from typing import Dict, Optional, Tuple

from common import OperatingSystem
from common.event_queue import IAgentEventPublisher
from common.types import AgentID, DiscoveredService, NetworkProtocol, NetworkService
from infection_monkey.i_puppet import FingerprintData, IFingerprinter, PingScanData, PortScanData

SSH_REGEX = r"SSH-\d\.\d-OpenSSH"
LINUX_DIST_SSH = ["ubuntu", "debian"]


class SSHFingerprinter(IFingerprinter):
    def __init__(self, agent_id: AgentID, agent_event_publisher: IAgentEventPublisher):
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher
        self._banner_regex = re.compile(SSH_REGEX, re.IGNORECASE)

    def get_host_fingerprint(
        self,
        host: str,
        _ping_scan_data: PingScanData,
        port_scan_data: Dict[int, PortScanData],
        _options: Dict,
    ) -> FingerprintData:
        os_type = None
        os_version = None
        services = []

        for ps_data in port_scan_data.values():
            if ps_data.banner and self._banner_regex.search(ps_data.banner):
                # TODO: We don't want to overwrite this in case one `ps_data` has
                #       the OS info and the next doesn't, the event will publish with
                #       whatever the last one has
                os_type, os_version = self._get_host_os(ps_data.banner)
                services.append(
                    DiscoveredService(
                        protocol=NetworkProtocol.TCP,
                        port=ps_data.port,
                        service=NetworkService.SSH,
                    )
                )

        return FingerprintData(os_type=os_type, os_version=os_version, services=services)

    @staticmethod
    def _get_host_os(banner) -> Tuple[Optional[OperatingSystem], Optional[str]]:
        os = None
        os_version = None
        for dist in LINUX_DIST_SSH:
            if banner.lower().find(dist) != -1:
                os_version = banner.split(" ").pop().strip()
                os = OperatingSystem.LINUX

        return os, os_version
