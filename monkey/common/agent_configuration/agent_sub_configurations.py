from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class CustomPBAConfiguration:
    """
    Dataclass for the configuration of custom post-breach actions

    Attributes:
        linux_command (str): Command to run on Linux victim machines. If a file is uploaded,
                             use this field to change its permissions, execute it, and/or delete
                             it.
                             Example: `chmod +x file.sh; ./file.sh; rm file.sh`
        linux_filename (str): Name of the file to upload on Linux victim machines.
                              Example: `i-am-custom-pba-file.sh`
        windows_command (str): Command to run on Windows victim machines. If a file is uploaded,
                               use this field to change its permissions, execute it, and/or delete
                               it.
                               Example: `file.bat & del file.bat`
        windows_filename (str): Name of the file to upload on Windows victim machines.
                                Example: `i-am-custom-pba-file.bat`
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
