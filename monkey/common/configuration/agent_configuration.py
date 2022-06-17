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
class ScanTargetConfiguration:
    blocked_ips: List[str]
    inaccessible_subnets: List[str]
    local_network_scan: bool
    subnets: List[str]


@dataclass(frozen=True)
class ICMPScanConfiguration:
    timeout_ms: int


class ICMPScanConfigurationSchema(Schema):
    timeout_ms = fields.Int()

    @post_load
    def _make_icmp_scan_configuration(self, data, **kwargs):
        return ICMPScanConfiguration(**data)


@dataclass(frozen=True)
class TCPScanConfiguration:
    timeout_ms: int
    ports: List[int]


class TCPScanConfigurationSchema(Schema):
    timeout_ms = fields.Int()
    ports = fields.List(fields.Int())

    @post_load
    def _make_tcp_scan_configuration(self, data, **kwargs):
        return TCPScanConfiguration(**data)
