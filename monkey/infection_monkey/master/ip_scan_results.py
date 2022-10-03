from dataclasses import dataclass
from typing import Dict

from common.types import NetworkPort, PingScanData
from infection_monkey.i_puppet import FingerprintData, PortScanData

FingerprinterName = str


@dataclass
class IPScanResults:
    ping_scan_data: PingScanData
    port_scan_data: Dict[NetworkPort, PortScanData]
    fingerprint_data: Dict[FingerprinterName, FingerprintData]
