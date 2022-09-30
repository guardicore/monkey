from typing import Tuple

from pydantic import confloat

from common.base_models import MutableInfectionMonkeyBaseModel

from .agent_sub_configurations import (
    CustomPBAConfiguration,
    PluginConfiguration,
    PropagationConfiguration,
)


class AgentConfiguration(MutableInfectionMonkeyBaseModel):
    keep_tunnel_open_time: confloat(ge=0)  # type: ignore[valid-type]
    custom_pbas: CustomPBAConfiguration
    post_breach_actions: Tuple[PluginConfiguration, ...]
    credential_collectors: Tuple[PluginConfiguration, ...]
    payloads: Tuple[PluginConfiguration, ...]
    propagation: PropagationConfiguration
