import re
import time
from ipaddress import IPv4Address
from typing import Dict, Optional, Sequence, Tuple

from monkeytypes import AgentID, DiscoveredService, NetworkProtocol, NetworkService, OperatingSystem

from common.agent_events import FingerprintingEvent
from common.event_queue import IAgentEventPublisher
from common.tags import ACTIVE_SCANNING_T1595_TAG, GATHER_VICTIM_HOST_INFORMATION_T1592_TAG
from infection_monkey.i_puppet import FingerprintData, IFingerprinter, PingScanData, PortScanData

SSH_REGEX = r"SSH-\d\.\d-OpenSSH"
LINUX_DIST_SSH = ["ubuntu", "debian"]

SSH_FINGERPRINTER_TAG = "ssh-fingerprinter"
EVENT_TAGS = frozenset(
    {SSH_FINGERPRINTER_TAG, ACTIVE_SCANNING_T1595_TAG, GATHER_VICTIM_HOST_INFORMATION_T1592_TAG}
)


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

        timestamp = time.time()
        for ps_data in port_scan_data.values():
            if ps_data.banner and self._banner_regex.search(ps_data.banner):
                if os_type is None and os_version is None:
                    os_type, os_version = self._get_host_os(ps_data.banner)
                services.append(
                    DiscoveredService(
                        protocol=NetworkProtocol.TCP,
                        port=ps_data.port,
                        service=NetworkService.SSH,
                    )
                )

        if len(services) > 0:
            # Even though there's no actual "event" taking place, we're still publishing a
            # FingerprintingEvent, as this is the only way for the Island to receive this module's
            # analysis. This ultimately a minor design flaw that can be addressed when/if we ever
            # get around to redesigning the scanning system/workflow.
            self._publish_fingerprinting_event(host, timestamp, os_type, os_version, services)

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

    def _publish_fingerprinting_event(
        self,
        host: str,
        timestamp: float,
        os_type: Optional[OperatingSystem],
        os_version: Optional[str],
        discovered_services: Sequence[DiscoveredService],
    ):
        self._agent_event_publisher.publish(
            FingerprintingEvent(
                source=self._agent_id,
                target=IPv4Address(host),
                timestamp=timestamp,
                tags=EVENT_TAGS,  # type: ignore [arg-type]
                os=os_type,
                os_version=os_version,
                discovered_services=tuple(discovered_services),
            )
        )
