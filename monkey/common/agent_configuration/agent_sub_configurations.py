from dataclasses import dataclass
from typing import Dict, Tuple


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
    blocked_ips: Tuple[str]
    inaccessible_subnets: Tuple[str]
    local_network_scan: bool
    subnets: Tuple[str]


@dataclass(frozen=True)
class ICMPScanConfiguration:
    timeout: float


@dataclass(frozen=True)
class TCPScanConfiguration:
    timeout: float
    ports: Tuple[int]


@dataclass(frozen=True)
class NetworkScanConfiguration:
    tcp: TCPScanConfiguration
    icmp: ICMPScanConfiguration
    fingerprinters: Tuple[PluginConfiguration]
    targets: ScanTargetConfiguration


@dataclass(frozen=True)
class ExploitationOptionsConfiguration:
    http_ports: Tuple[int]


@dataclass(frozen=True)
class ExploitationConfiguration:
    options: ExploitationOptionsConfiguration
    brute_force: Tuple[PluginConfiguration]
    vulnerability: Tuple[PluginConfiguration]


@dataclass(frozen=True)
class PropagationConfiguration:
    maximum_depth: int
    network_scan: NetworkScanConfiguration
    exploitation: ExploitationConfiguration
