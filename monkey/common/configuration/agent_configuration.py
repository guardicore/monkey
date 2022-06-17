from dataclasses import dataclass
from typing import Dict, List

from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField

from common import OperatingSystems


@dataclass(frozen=True)
class CustomPBAConfiguration:
    linux_command: str
    linux_filename: str
    windows_command: str
    windows_filename: str


class CustomPBAConfigurationSchema(Schema):
    linux_command = fields.Str()
    linux_filename = fields.Str()
    windows_command = fields.Str()
    windows_filename = fields.Str()

    @post_load
    def _make_custom_pba_configuration(self, data, **kwargs):
        return CustomPBAConfiguration(**data)


@dataclass(frozen=True)
class PluginConfiguration:
    name: str
    options: Dict


class PluginConfigurationSchema(Schema):
    name = fields.Str()
    options = fields.Mapping()

    @post_load
    def _make_plugin_configuration(self, data, **kwargs):
        return PluginConfiguration(**data)


@dataclass(frozen=True)
class ExploitationOptionsConfiguration:
    http_ports: List[int]


@dataclass(frozen=True)
class ScanTargetConfiguration:
    blocked_ips: List[str]
    inaccessible_subnets: List[str]
    local_network_scan: bool
    subnets: List[str]


class ScanTargetConfigurationSchema(Schema):
    blocked_ips = fields.List(fields.Str())
    inaccessible_subnets = fields.List(fields.Str())
    local_network_scan = fields.Bool()
    subnets = fields.List(fields.Str())

    @post_load
    def _make_scan_target_configuration(self, data, **kwargs):
        return ScanTargetConfiguration(**data)


@dataclass(frozen=True)
class ICMPScanConfiguration:
    timeout: float


class ICMPScanConfigurationSchema(Schema):
    timeout = fields.Float()

    @post_load
    def _make_icmp_scan_configuration(self, data, **kwargs):
        return ICMPScanConfiguration(**data)


@dataclass(frozen=True)
class TCPScanConfiguration:
    timeout: float
    ports: List[int]


class TCPScanConfigurationSchema(Schema):
    timeout = fields.Float()
    ports = fields.List(fields.Int())

    @post_load
    def _make_tcp_scan_configuration(self, data, **kwargs):
        return TCPScanConfiguration(**data)


@dataclass(frozen=True)
class NetworkScanConfiguration:
    tcp: TCPScanConfiguration
    icmp: ICMPScanConfiguration
    fingerprinters: List[PluginConfiguration]
    targets: ScanTargetConfiguration


class NetworkScanConfigurationSchema(Schema):
    tcp = fields.Nested(TCPScanConfigurationSchema)
    icmp = fields.Nested(ICMPScanConfigurationSchema)
    fingerprinters = fields.List(fields.Nested(PluginConfigurationSchema))
    targets = fields.Nested(ScanTargetConfigurationSchema)

    @post_load
    def _make_network_scan_configuration(self, data, **kwargs):
        return NetworkScanConfiguration(**data)


class ExploitationOptionsConfigurationSchema(Schema):
    http_ports = fields.List(fields.Int())

    @post_load
    def _make_exploitation_options_configuration(self, data, **kwargs):
        return ExploitationOptionsConfiguration(**data)


@dataclass(frozen=True)
class ExploiterConfiguration:
    name: str
    options: Dict
    supported_os: List[OperatingSystems]


class ExploiterConfigurationSchema(Schema):
    name = fields.Str()
    options = fields.Mapping()
    supported_os = fields.List(EnumField(OperatingSystems))

    @post_load
    def _make_exploiter_configuration(self, data, **kwargs):
        return ExploiterConfiguration(**data)


@dataclass(frozen=True)
class ExploitationConfiguration:
    options: ExploitationOptionsConfiguration
    brute_force: List[ExploiterConfiguration]
    vulnerability: List[ExploiterConfiguration]


class ExploitationConfigurationSchema(Schema):
    options = fields.Nested(ExploitationOptionsConfigurationSchema)
    brute_force = fields.List(fields.Nested(ExploiterConfigurationSchema))
    vulnerability = fields.List(fields.Nested(ExploiterConfigurationSchema))

    @post_load
    def _make_exploitation_options_configuration(self, data, **kwargs):
        return ExploitationConfiguration(**data)


@dataclass(frozen=True)
class PropagationConfiguration:
    maximum_depth: int
    network_scan: NetworkScanConfiguration
    exploitation: ExploitationConfiguration


class PropagationConfigurationSchema(Schema):
    maximum_depth = fields.Int()
    network_scan = fields.Nested(NetworkScanConfigurationSchema)
    exploitation = fields.Nested(ExploitationConfigurationSchema)

    @post_load
    def _make_propagation_configuration(self, data, **kwargs):
        return PropagationConfiguration(**data)


@dataclass(frozen=True)
class AgentConfiguration:
    keep_tunnel_open_time: float
    custom_pbas: CustomPBAConfiguration
    post_breach_actions: List[PluginConfiguration]
    credential_collectors: List[PluginConfiguration]
    payloads: List[PluginConfiguration]
    propagation: PropagationConfiguration


class AgentConfigurationSchema(Schema):
    keep_tunnel_open_time = fields.Float()
    custom_pbas = fields.Nested(CustomPBAConfigurationSchema)
    post_breach_actions = fields.List(fields.Nested(PluginConfigurationSchema))
    credential_collectors = fields.List(fields.Nested(PluginConfigurationSchema))
    payloads = fields.List(fields.Nested(PluginConfigurationSchema))
    propagation = fields.Nested(PropagationConfigurationSchema)

    @post_load
    def _make_agent_configuration(self, data, **kwargs):
        return AgentConfiguration(**data)
