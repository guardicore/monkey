from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class CustomPBAConfiguration:
    """
    A configuration for custom post-breach actions

    Attributes:
        :param linux_command: Command to run on Linux victim machines. If a file is uploaded,
                              use this field to change its permissions, execute it, and/or delete
                              it.
                              Example: `chmod +x file.sh; ./file.sh; rm file.sh`
        :param linux_filename: Name of the file to upload on Linux victim machines.
        :param windows_command: Command to run on Windows victim machines. If a file is uploaded,
                                use this field to change its permissions, execute it, and/or delete
                                it.
                                Example: `file.bat & del file.bat`
        :param windows_filename: Name of the file to upload on Windows victim machines.
    """

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
    blocked_ips: Tuple[str, ...]
    inaccessible_subnets: Tuple[str, ...]
    local_network_scan: bool
    subnets: Tuple[str, ...]


@dataclass(frozen=True)
class ICMPScanConfiguration:
    timeout: float


@dataclass(frozen=True)
class TCPScanConfiguration:
    timeout: float
    ports: Tuple[int, ...]


@dataclass(frozen=True)
class NetworkScanConfiguration:
    tcp: TCPScanConfiguration
    icmp: ICMPScanConfiguration
    fingerprinters: Tuple[PluginConfiguration, ...]
    targets: ScanTargetConfiguration


@dataclass(frozen=True)
class ExploitationOptionsConfiguration:
    http_ports: Tuple[int, ...]


@dataclass(frozen=True)
class ExploitationConfiguration:
    options: ExploitationOptionsConfiguration
    brute_force: Tuple[PluginConfiguration, ...]
    vulnerability: Tuple[PluginConfiguration, ...]


@dataclass(frozen=True)
class PropagationConfiguration:
    maximum_depth: int
    network_scan: NetworkScanConfiguration
    exploitation: ExploitationConfiguration
