from marshmallow import Schema, fields, post_load, validate

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
from .validators.filenames import validate_linux_filename, validate_windows_filename
from .validators.ip_ranges import validate_ip, validate_subnet_range


class CustomPBAConfigurationSchema(Schema):
    linux_command = fields.Str()
    linux_filename = fields.Str(validate=validate_linux_filename)
    windows_command = fields.Str()
    windows_filename = fields.Str(validate=validate_windows_filename)

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
    blocked_ips = fields.List(fields.Str(validate=validate_ip))
    inaccessible_subnets = fields.List(fields.Str(validate=validate_subnet_range))
    local_network_scan = fields.Bool()
    subnets = fields.List(fields.Str(validate=validate_subnet_range))

    @post_load
    @freeze_lists
    def _make_scan_target_configuration(self, data, **kwargs):
        return ScanTargetConfiguration(**data)


class ICMPScanConfigurationSchema(Schema):
    timeout = fields.Float(validate=validate.Range(min=0))

    @post_load
    def _make_icmp_scan_configuration(self, data, **kwargs):
        return ICMPScanConfiguration(**data)


class TCPScanConfigurationSchema(Schema):
    timeout = fields.Float(validate=validate.Range(min=0))
    ports = fields.List(fields.Int(validate=validate.Range(min=0, max=65535)))

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
    http_ports = fields.List(fields.Int(validate=validate.Range(min=0, max=65535)))

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
    maximum_depth = fields.Int(validate=validate.Range(min=0))
    network_scan = fields.Nested(NetworkScanConfigurationSchema)
    exploitation = fields.Nested(ExploitationConfigurationSchema)

    @post_load
    def _make_propagation_configuration(self, data, **kwargs):
        return PropagationConfiguration(**data)
