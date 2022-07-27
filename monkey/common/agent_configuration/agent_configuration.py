from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple

from marshmallow import Schema, fields, validate
from marshmallow.exceptions import MarshmallowError

from ..utils.code_utils import freeze_lists_in_mapping
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
    def __init__(self, message: str):
        self._message = message

    def __str__(self) -> str:
        return (
            f"Cannot construct an AgentConfiguration object with the supplied, invalid data: "
            f"{self._message}"
        )


@dataclass(frozen=True)
class AgentConfiguration:
    """
    A configuration for Infection Monkey agents

    Attributes:
        :param keep_tunnel_open_time: Maximum time in seconds to keep a tunnel open after
                                      the last exploit
        :param custom_pbas: Configuration for custom post-breach actions
        :param post_breach_actions: Configuration for post-breach actions
        :param credential_collectors: Configuration for credential collectors
        :param payloads: Configuration for payloads
        :param propagation: Configuration for propagation
    """

    keep_tunnel_open_time: float
    custom_pbas: CustomPBAConfiguration
    post_breach_actions: Tuple[PluginConfiguration, ...]
    credential_collectors: Tuple[PluginConfiguration, ...]
    payloads: Tuple[PluginConfiguration, ...]
    propagation: PropagationConfiguration

    def __post_init__(self):
        # This will raise an exception if the object is invalid. Calling this in __post__init()
        # makes it impossible to construct an invalid object
        try:
            AgentConfigurationSchema().dump(self)
        except Exception as err:
            raise InvalidConfigurationError(str(err))

    @staticmethod
    def from_mapping(config_mapping: Mapping[str, Any]) -> AgentConfiguration:
        """
        Construct an AgentConfiguration from a Mapping

        :param config_mapping: A Mapping that represents an AgentConfiguration
        :return: An AgentConfiguration
        :raises: InvalidConfigurationError if the provided Mapping does not represent a valid
                 AgentConfiguration
        """

        try:
            config_dict = AgentConfigurationSchema().load(config_mapping)
            config_dict = freeze_lists_in_mapping(config_dict)
            return AgentConfiguration(**config_dict)
        except MarshmallowError as err:
            raise InvalidConfigurationError(str(err))

    @staticmethod
    def from_json(config_json: str) -> AgentConfiguration:
        """
        Construct an AgentConfiguration from a JSON string

        :param config_json: A JSON string that represents an AgentConfiguration
        :return: An AgentConfiguration
        :raises: InvalidConfigurationError if the provided JSON does not represent a valid
                 AgentConfiguration
        """
        try:
            config_dict = AgentConfigurationSchema().loads(config_json)
            config_dict = freeze_lists_in_mapping(config_dict)
            return AgentConfiguration(**config_dict)
        except MarshmallowError as err:
            raise InvalidConfigurationError(str(err))

    @staticmethod
    def to_mapping(config: AgentConfiguration) -> Mapping[str, Any]:
        """
        Serialize an AgentConfiguration to a Mapping

        :param config: An AgentConfiguration
        :return: A Mapping that represents the AgentConfiguration
        """
        return AgentConfigurationSchema().dump(config)

    @staticmethod
    def to_json(config: AgentConfiguration) -> str:
        """
        Serialize an AgentConfiguration to JSON

        :param config: An AgentConfiguration
        :return: A JSON string that represents the AgentConfiguration
        """
        return AgentConfigurationSchema().dumps(config)


class AgentConfigurationSchema(Schema):
    keep_tunnel_open_time = fields.Float(validate=validate.Range(min=0))
    custom_pbas = fields.Nested(CustomPBAConfigurationSchema)
    post_breach_actions = fields.List(fields.Nested(PluginConfigurationSchema))
    credential_collectors = fields.List(fields.Nested(PluginConfigurationSchema))
    payloads = fields.List(fields.Nested(PluginConfigurationSchema))
    propagation = fields.Nested(PropagationConfigurationSchema)
