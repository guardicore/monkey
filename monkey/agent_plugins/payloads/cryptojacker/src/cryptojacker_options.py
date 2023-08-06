from pydantic import Field

from common.base_models import InfectionMonkeyBaseModel
from common.types import PercentLimited


class CryptojackerOptions(InfectionMonkeyBaseModel):
    duration: float = Field(
        title="Duration",
        description="The duration (in seconds) for which the cryptojacking simulation should run"
        " on each machine",
        default=300,  # 5 minutes
        ge=0,
    )
    cpu_utilization: PercentLimited = Field(  # type: ignore[valid-type]
        title="CPU utilization",
        description="The percentage of CPU to use on a machine",
        default=80,
    )
    memory_utilization: PercentLimited = Field(  # type: ignore[valid-type]
        title="Memory utilization",
        description="The percentage of memory to use on a machine",
        default=20,
    )
    simulate_bitcoin_mining_network_traffic: bool = Field(
        title="Simulate Bitcoin mining network traffic",
        default=False,
        description="If enabled, the Agent will periodically send requests used in Bitcoin mining"
        " over the network.",
    )
