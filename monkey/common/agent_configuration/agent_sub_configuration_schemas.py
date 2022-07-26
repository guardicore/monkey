from marshmallow import Schema, fields, post_load

from .agent_sub_configurations import (
    CustomPBAConfiguration,
    ExploitationConfiguration,
    ExploitationOptionsConfiguration,
    ICMPScanConfiguration,
    NetworkScanConfiguration,
    PluginConfiguration,
    PropagationConfiguration,
    ScanTargetConfiguration,
    TCPScanConfiguration,
)
from .utils import freeze_lists


class CustomPBAConfigurationSchema(Schema):
    linux_command = fields.Str()
    linux_filename = fields.Str()
    windows_command = fields.Str()
    windows_filename = fields.Str()

    @post_load
    def _make_custom_pba_configuration(self, data, **kwargs):
        return CustomPBAConfiguration(**data)


class PluginConfigurationSchema(Schema):
    name = fields.Str()
    options = fields.Mapping()

    @post_load
    def _make_plugin_configuration(self, data, **kwargs):
        return PluginConfiguration(**data)


class ScanTargetConfigurationSchema(Schema):
    blocked_ips = fields.List(fields.Str())
    inaccessible_subnets = fields.List(fields.Str())
    local_network_scan = fields.Bool()
    subnets = fields.List(fields.Str())

    @post_load
    @freeze_lists
    def _make_scan_target_configuration(self, data, **kwargs):
        return ScanTargetConfiguration(**data)


class ICMPScanConfigurationSchema(Schema):
    timeout = fields.Float()

    @post_load
    def _make_icmp_scan_configuration(self, data, **kwargs):
        return ICMPScanConfiguration(**data)


class TCPScanConfigurationSchema(Schema):
    timeout = fields.Float()
    ports = fields.List(fields.Int())

    @post_load
    @freeze_lists
    def _make_tcp_scan_configuration(self, data, **kwargs):
        return TCPScanConfiguration(**data)


class NetworkScanConfigurationSchema(Schema):
    tcp = fields.Nested(TCPScanConfigurationSchema)
    icmp = fields.Nested(ICMPScanConfigurationSchema)
    fingerprinters = fields.List(fields.Nested(PluginConfigurationSchema))
    targets = fields.Nested(ScanTargetConfigurationSchema)

    @post_load
    @freeze_lists
    def _make_network_scan_configuration(self, data, **kwargs):
        return NetworkScanConfiguration(**data)


class ExploitationOptionsConfigurationSchema(Schema):
    http_ports = fields.List(fields.Int())

    @post_load
    @freeze_lists
    def _make_exploitation_options_configuration(self, data, **kwargs):
        return ExploitationOptionsConfiguration(**data)


class ExploitationConfigurationSchema(Schema):
    options = fields.Nested(ExploitationOptionsConfigurationSchema)
    brute_force = fields.List(fields.Nested(PluginConfigurationSchema))
    vulnerability = fields.List(fields.Nested(PluginConfigurationSchema))

    @post_load
    @freeze_lists
    def _make_exploitation_options_configuration(self, data, **kwargs):
        return ExploitationConfiguration(**data)


class PropagationConfigurationSchema(Schema):
    maximum_depth = fields.Int()
    network_scan = fields.Nested(NetworkScanConfigurationSchema)
    exploitation = fields.Nested(ExploitationConfigurationSchema)

    @post_load
    def _make_propagation_configuration(self, data, **kwargs):
        return PropagationConfiguration(**data)
