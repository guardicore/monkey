import re

from marshmallow import Schema, ValidationError, fields, post_load, validate, validates

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

valid_windows_custom_pba_filename_regex = re.compile(r"^[^<>:\"\\\/|?*]*[^<>:\"\\\/|?* \.]+$|^$")
valid_linux_custom_pba_filename_regex = re.compile(r"^[^\0/]*$")


class CustomPBAConfigurationSchema(Schema):
    linux_command = fields.Str()
    linux_filename = fields.Str(
        validate=validate.Regexp(regex=valid_linux_custom_pba_filename_regex)
    )
    windows_command = fields.Str()
    windows_filename = fields.Str(
        validate=validate.Regexp(regex=valid_windows_custom_pba_filename_regex)
    )

    @validates("windows_filename")
    def validate_windows_filename_not_reserved(self, windows_filename):
        # filename shouldn't start with any of these and be followed by a period
        if windows_filename.split(".")[0].upper() in [
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        ]:
            raise ValidationError("Invalid Windows filename: reserved name used")

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
    maximum_depth = fields.Int(validate=validate.Range(min=0))
    network_scan = fields.Nested(NetworkScanConfigurationSchema)
    exploitation = fields.Nested(ExploitationConfigurationSchema)

    @post_load
    def _make_propagation_configuration(self, data, **kwargs):
        return PropagationConfiguration(**data)
