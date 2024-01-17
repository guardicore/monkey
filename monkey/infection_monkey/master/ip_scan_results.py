from dataclasses import dataclass
from typing import Dict

from agentpluginapi import PortScanDataDict

from infection_monkey.i_puppet import FingerprintData, PingScanData

FingerprinterName = str


@dataclass
class IPScanResults:
    ping_scan_data: PingScanData
    port_scan_data: PortScanDataDict
    fingerprint_data: Dict[FingerprinterName, FingerprintData]
