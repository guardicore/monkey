from dataclasses import dataclass
from typing import Dict, List

from common import OperatingSystems


@dataclass(frozen=True)
class CustomPBAConfiguration:
    linux_command: str
    linux_filename: str
    windows_command: str
    windows_filename: str


@dataclass(frozen=True)
class PluginConfiguration:
    name: str
    options: Dict


@dataclass(frozen=True)
class ScanTargetConfiguration:
    blocked_ips: List[str]
    inaccessible_subnets: List[str]
    local_network_scan: bool
    subnets: List[str]


@dataclass(frozen=True)
class ICMPScanConfiguration:
    timeout: float


@dataclass(frozen=True)
class TCPScanConfiguration:
    timeout: float
    ports: List[int]


@dataclass(frozen=True)
class NetworkScanConfiguration:
    tcp: TCPScanConfiguration
    icmp: ICMPScanConfiguration
    fingerprinters: List[PluginConfiguration]
    targets: ScanTargetConfiguration


@dataclass(frozen=True)
class ExploitationOptionsConfiguration:
    http_ports: List[int]


@dataclass(frozen=True)
class ExploiterConfiguration:
    name: str
    options: Dict
    supported_os: List[OperatingSystems]


@dataclass(frozen=True)
class ExploitationConfiguration:
    options: ExploitationOptionsConfiguration
    brute_force: List[ExploiterConfiguration]
    vulnerability: List[ExploiterConfiguration]


@dataclass(frozen=True)
class PropagationConfiguration:
    maximum_depth: int
    network_scan: NetworkScanConfiguration
    exploitation: ExploitationConfiguration
