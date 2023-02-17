import re
from typing import Dict, Optional, Tuple

from common import OperatingSystem
from infection_monkey.dataclasses import PortScanData
from infection_monkey.i_puppet import FingerprintData, IFingerprinter, PingScanData

SSH_REGEX = r"SSH-\d\.\d-OpenSSH"
LINUX_DIST_SSH = ["ubuntu", "debian"]
DISPLAY_NAME = "SSH"


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
        services = {}

        for ps_data in port_scan_data.values():
            if ps_data.banner and self._banner_regex.search(ps_data.banner):
                os_type, os_version = self._get_host_os(ps_data.banner)
                services[f"tcp-{ps_data.port}"] = {
                    "display_name": DISPLAY_NAME,
                    "port": ps_data.port,
                    "name": "ssh",
                }
        return FingerprintData(os_type, os_version, services)

    @staticmethod
    def _get_host_os(banner) -> Tuple[Optional[str], Optional[str]]:
        os = None
        os_version = None
        for dist in LINUX_DIST_SSH:
            if banner.lower().find(dist) != -1:
                os_version = banner.split(" ").pop().strip()
                os = OperatingSystem.LINUX

        return os, os_version
