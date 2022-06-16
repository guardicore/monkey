from dataclasses import dataclass
from typing import Dict

from marshmallow import RAISE, Schema, fields, post_load


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
