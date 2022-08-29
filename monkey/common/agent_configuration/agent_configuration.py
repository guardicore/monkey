from __future__ import annotations

from typing import Tuple

from pydantic import PositiveFloat

from common.base_models import MutableInfectionMonkeyBaseModel

from .agent_sub_configurations import (
    Pydantic___CustomPBAConfiguration,
    Pydantic___PluginConfiguration,
    Pydantic___PropagationConfiguration,
)


class InvalidConfigurationError(Exception):
    def __init__(self, message: str):
        self._message = message

    def __str__(self) -> str:
        return (
            f"Cannot construct an AgentConfiguration object with the supplied, invalid data: "
            f"{self._message}"
        )


class Pydantic___AgentConfiguration(MutableInfectionMonkeyBaseModel):
    keep_tunnel_open_time: PositiveFloat
    custom_pbas: Pydantic___CustomPBAConfiguration
    post_breach_actions: Tuple[Pydantic___PluginConfiguration, ...]
    credential_collectors: Tuple[Pydantic___PluginConfiguration, ...]
    payloads: Tuple[Pydantic___PluginConfiguration, ...]
    propagation: Pydantic___PropagationConfiguration
