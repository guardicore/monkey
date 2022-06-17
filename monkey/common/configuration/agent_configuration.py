from dataclasses import dataclass
from typing import Dict, List

from marshmallow import RAISE, Schema, fields, post_load
from marshmallow_enum import EnumField

from common import OperatingSystems


@dataclass(frozen=True)
class CustomPBAConfiguration:
    linux_command: str
    linux_filename: str
    windows_command: str
    windows_filename: str


class CustomPBAConfigurationSchema(Schema):
    class Meta:
        unknown = RAISE

    linux_command = fields.Str()
    linux_filename = fields.Str()
    windows_command = fields.Str()
    windows_filename = fields.Str()

    @post_load
    def make_custom_pba_configuration(self, data, **kwargs):
        return CustomPBAConfiguration(**data)


@dataclass(frozen=True)
class PluginConfiguration:
    name: str
    options: Dict


class PluginConfigurationSchema(Schema):
    class Meta:
        unknown = RAISE

    name = fields.Str()
    options = fields.Mapping()

    @post_load
    def make_plugin_configuration(self, data, **kwargs):
        return PluginConfiguration(**data)


@dataclass(frozen=True)
class ExploitationOptionsConfiguration:
    http_ports: List[int]


class ExploitationOptionsConfigurationSchema(Schema):
    http_ports = fields.List(fields.Int())

    @post_load
    def make_exploitation_options_configuration(self, data, **kwargs):
        return ExploitationOptionsConfiguration(**data)


@dataclass(frozen=True)
class ExploiterConfiguration:
    name: str
    options: Dict
    supported_os: List[OperatingSystems]


class ExploiterConfigurationSchema(Schema):
    class Meta:
        unknown = RAISE

    name = fields.Str()
    options = fields.Mapping()
    supported_os = fields.List(EnumField(OperatingSystems))

    @post_load
    def make_exploiter_configuration(self, data, **kwargs):
        return ExploiterConfiguration(**data)
