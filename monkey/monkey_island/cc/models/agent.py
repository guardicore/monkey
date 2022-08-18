from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from . import MachineID
from .base_models import MutableBaseModel


class Agent(MutableBaseModel):
    id: UUID = Field(..., allow_mutation=False)
    machine_id: MachineID = Field(..., allow_mutation=False)
    start_time: datetime = Field(..., allow_mutation=False)
    stop_time: Optional[datetime]
    parent_id: UUID = Field(..., allow_mutation=False)
    cc_server: str = Field(default="")
    log_contents: str = Field(default="")
