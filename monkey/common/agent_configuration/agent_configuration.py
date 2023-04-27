from typing import Dict

from pydantic import Field, confloat

from common.base_models import MutableInfectionMonkeyBaseModel

from .agent_sub_configurations import PropagationConfiguration


class AgentConfiguration(MutableInfectionMonkeyBaseModel):
    keep_tunnel_open_time: confloat(ge=0) = Field(  # type: ignore[valid-type]
        title="Keep tunnel open time",
        description="Time to keep tunnel open before "
        "going down after last exploit (in "
        "seconds)",
        default=30,
    )
    credentials_collectors: Dict[str, Dict] = Field(
        title="Enabled credentials collectors",
        description="Click on a credentials collectors to get more information"
        " about it. \n \u26A0 Note that using unsafe options may"
        " result in unexpected behavior on the machine.",
    )
    payloads: Dict[str, Dict] = Field(
        title="Payloads", description="Configure payloads that Agents will execute"
    )
    propagation: PropagationConfiguration = Field(
        title="Propagation",
        description="Configure options for the attack’s propagation stage",
    )
