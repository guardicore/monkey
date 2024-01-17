from dataclasses import dataclass
from typing import Dict

from agentpluginapi import PingScanData, PortScanDataDict

from infection_monkey.i_puppet import FingerprintData

FingerprinterName = str


@dataclass
class IPScanResults:
    ping_scan_data: PingScanData
    port_scan_data: PortScanDataDict
    fingerprint_data: Dict[FingerprinterName, FingerprintData]
