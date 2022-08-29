from __future__ import annotations

from typing import Tuple

from pydantic import PositiveFloat

from common.base_models import MutableInfectionMonkeyBaseModel

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


class AgentConfiguration(MutableInfectionMonkeyBaseModel):
    keep_tunnel_open_time: PositiveFloat
    custom_pbas: CustomPBAConfiguration
    post_breach_actions: Tuple[PluginConfiguration, ...]
    credential_collectors: Tuple[PluginConfiguration, ...]
    payloads: Tuple[PluginConfiguration, ...]
    propagation: PropagationConfiguration
