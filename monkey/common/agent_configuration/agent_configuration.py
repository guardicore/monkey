from typing import Dict

from monkeytypes.base_models import MutableInfectionMonkeyBaseModel
from pydantic import Field
from typing_extensions import Annotated

from .agent_sub_configurations import PolymorphismConfiguration, PropagationConfiguration


class AgentConfiguration(MutableInfectionMonkeyBaseModel):
    keep_tunnel_open_time: Annotated[float, Field(ge=0)] = Field(
        title="Keep tunnel open time",
        description="Time to keep tunnel open before "
        "going down after last exploit (in "
        "seconds)",
        default=30,
    )
    credentials_collectors: Dict[str, Dict] = Field(
        title="Enabled credentials collectors",
        description="Click on a credentials collector to get more information"
        " about it. \n \u26A0 Note that using unsafe options may"
        " result in unexpected behavior on the machine.",
    )
    payloads: Dict[str, Dict] = Field(
        title="Enabled payloads",
        description="Click on a payload to get more information"
        " about it. \n \u26A0 Note that using unsafe options may"
        " result in unexpected behavior on the machine.",
    )
    propagation: PropagationConfiguration = Field(
        title="Propagation",
        description="Configure options for the attack’s propagation stage",
    )
    polymorphism: PolymorphismConfiguration = Field(
        title="Emulate polymorphism",
        description="Emulate polymorphic (or metamorphic) malware by"
        " modifying the Agent binary before propagation.",
    )
