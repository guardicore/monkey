import re
from typing import Dict, Optional, Tuple

from common import OperatingSystem
from common.types import DiscoveredService, NetworkProtocol, NetworkService
from infection_monkey.i_puppet import FingerprintData, IFingerprinter, PingScanData, PortScanData

SSH_REGEX = r"SSH-\d\.\d-OpenSSH"
LINUX_DIST_SSH = ["ubuntu", "debian"]


class SSHFingerprinter(IFingerprinter):
    def __init__(self):
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
