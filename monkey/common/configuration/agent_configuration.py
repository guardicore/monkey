from dataclasses import dataclass

from marshmallow import RAISE, Schema, fields, post_load


@dataclass(frozen=True)
class PluginConfiguration:
    name: str
    options: dict


class PluginConfigurationSchema(Schema):
    class Meta:
        unknown = RAISE

    name = fields.Str()
    options = fields.Mapping()

    @post_load
    def make_plugin_configuration(self, data, **kwargs):
        return PluginConfiguration(**data)
