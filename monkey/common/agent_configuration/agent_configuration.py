from typing import Dict, Optional

from pydantic import Field, confloat

from common.base_models import MutableInfectionMonkeyBaseModel

from .agent_sub_configurations import CredentialsCollectorsConfiguration, PropagationConfiguration


class AgentConfiguration(MutableInfectionMonkeyBaseModel):
    keep_tunnel_open_time: confloat(ge=0) = Field(  # type: ignore[valid-type]
        title="Keep tunnel open time",
        description="Time to keep tunnel open before "
        "going down after last exploit (in "
        "seconds)",
        default=30,
    )
    credentials_collectors: Optional[CredentialsCollectorsConfiguration] = Field(
        title="Credentials collectors",
        description="Configure options for the attack’s credentials collection stage",
    )
    payloads: Dict[str, Dict] = Field(
        title="Payloads", description="Configure payloads that Agents will execute"
    )
    propagation: PropagationConfiguration = Field(
        title="Propagation",
        description="Configure options for the attack’s propagation stage",
    )
