from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field
from typing_extensions import TypeAlias

from common.base_models import MutableInfectionMonkeyBaseModel

from . import MachineID

AgentID: TypeAlias = UUID


class Agent(MutableInfectionMonkeyBaseModel):
    id: AgentID = Field(..., allow_mutation=False)
    machine_id: MachineID = Field(..., allow_mutation=False)
    start_time: datetime = Field(..., allow_mutation=False)
    stop_time: Optional[datetime]
    parent_id: Optional[AgentID] = Field(allow_mutation=False)
    cc_server: str = Field(default="")
    log_contents: str = Field(default="")
