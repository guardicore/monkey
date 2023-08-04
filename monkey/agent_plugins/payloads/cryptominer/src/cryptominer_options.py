from pydantic import Field, conint

from common.base_models import InfectionMonkeyBaseModel


class CryptominerOptions(InfectionMonkeyBaseModel):
    simulation_time: float = Field(
        title="Simulation time",
        description="The time (in seconds) for which the cryptomining simulation should run"
        " on each machine",
        default=0,
        ge=0,
    )
    cpu_utilization: conint(ge=0, le=100) = Field(  # type: ignore[valid-type]
        title="CPU utilization",
        description="The percentage of CPU to use on a machine",
        default=20,
    )
    memory_utilization: conint(ge=0, le=100) = Field(  # type: ignore[valid-type]
        title="Memory utilization",
        description="The percentage of memory to use on a machine",
        default=20,
    )
    send_dummy_request: bool = Field(
        title="Send dummy cryptomining request",
        default=False,
        description="If enabled, the Agent will send a request with the method `getblocktemplate`"
        " to the Island",
    )
