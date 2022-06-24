from __future__ import annotations

from dataclasses import dataclass
from typing import List

from marshmallow import Schema, fields
from marshmallow.exceptions import MarshmallowError

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


class InvalidConfigurationError(Exception):
    pass


INVALID_CONFIGURATION_ERROR_MESSAGE = (
    "Cannot construct an AgentConfiguration object with the supplied, invalid data:"
)


@dataclass(frozen=True)
class AgentConfiguration:
    keep_tunnel_open_time: float
    custom_pbas: CustomPBAConfiguration
    post_breach_actions: List[PluginConfiguration]
    credential_collectors: List[PluginConfiguration]
    payloads: List[PluginConfiguration]
    propagation: PropagationConfiguration

    def __post_init__(self):
        # This will raise an exception if the object is invalid. Calling this in __post__init()
        # makes it impossible to construct an invalid object
        try:
            AgentConfigurationSchema().dump(self)
        except Exception as err:
            raise InvalidConfigurationError(f"{INVALID_CONFIGURATION_ERROR_MESSAGE}: {err}")

    @staticmethod
    def from_dict(dict_: dict):
        try:
            config_dict = AgentConfigurationSchema().load(dict_)
            return AgentConfiguration(**config_dict)
        except MarshmallowError as err:
            raise InvalidConfigurationError(f"{INVALID_CONFIGURATION_ERROR_MESSAGE}: {err}")

    @staticmethod
    def from_json(config_json: dict):
        try:
            config_dict = AgentConfigurationSchema().loads(config_json)
            return AgentConfiguration(**config_dict)
        except MarshmallowError as err:
            raise InvalidConfigurationError(f"{INVALID_CONFIGURATION_ERROR_MESSAGE}: {err}")

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
