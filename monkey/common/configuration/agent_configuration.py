from __future__ import annotations

from dataclasses import dataclass
from typing import List

from marshmallow import Schema, fields, post_load

from .agent_sub_configuration_schemas import (
    CustomPBAConfigurationSchema,
    PluginConfigurationSchema,
    PropagationConfigurationSchema,
)
from .agent_sub_configurations import (
    CustomPBAConfiguration,
    PluginConfiguration,
    PropagationConfiguration,
)


@dataclass(frozen=True)
class AgentConfiguration:
    keep_tunnel_open_time: float
    custom_pbas: CustomPBAConfiguration
    post_breach_actions: List[PluginConfiguration]
    credential_collectors: List[PluginConfiguration]
    payloads: List[PluginConfiguration]
    propagation: PropagationConfiguration

    @staticmethod
    def from_dict(dict_: dict):
        return AgentConfigurationSchema().load(dict_)

    @staticmethod
    def from_json(config_json: dict):
        return AgentConfigurationSchema().loads(config_json)

    @staticmethod
    def to_json(config: AgentConfiguration) -> str:
        return AgentConfigurationSchema().dumps(config)


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
