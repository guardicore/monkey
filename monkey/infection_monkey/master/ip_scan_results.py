from dataclasses import dataclass
from typing import Dict

from common.types import NetworkPort
from infection_monkey.dataclasses import FingerprintData, PingScanData, PortScanData

FingerprinterName = str


@dataclass
class IPScanResults:
    ping_scan_data: PingScanData
    port_scan_data: Dict[NetworkPort, PortScanData]
    fingerprint_data: Dict[FingerprinterName, FingerprintData]
