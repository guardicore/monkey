import re
from typing import Dict, Tuple, Union

from infection_monkey.i_puppet import FingerprintData, IFingerprinter, PortScanData

SSH_PORT = 22
SSH_REGEX = r"SSH-\d\.\d-OpenSSH"
LINUX_DIST_SSH = ["ubuntu", "debian"]


class SSHFingerprinter(IFingerprinter):
    _SCANNED_SERVICE = "SSH"

    def __init__(self):
        self._banner_regex = re.compile(SSH_REGEX, re.IGNORECASE)

    def get_host_fingerprint(
        self, host: str, _ping_scan_data, port_scan_data: Dict[int, PortScanData], _options
    ) -> FingerprintData:
        os_type = None
        os_version = None
        services = {}

        for ps_data in list(port_scan_data.values()):
            if ps_data.banner and self._banner_regex.search(ps_data.banner):
                os_type, os_version = self._get_host_os(ps_data.banner)
                services[f"tcp-{ps_data.port}"] = {
                    "display_name": SSHFingerprinter._SCANNED_SERVICE,
                    "port": ps_data.port,
                    "name": "ssh",
                }
        return FingerprintData(os_type, os_version, services)

    @staticmethod
    def _get_host_os(banner) -> Tuple[Union[str, None], Union[str, None]]:
        os = None
        os_version = None
        for dist in LINUX_DIST_SSH:
            if banner.lower().find(dist) != -1:
                os_version = banner.split(" ").pop().strip()
                os = "linux"

        return os, os_version
