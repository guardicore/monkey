from datetime import datetime
from typing import Optional

from monkeytypes import MutableInfectionMonkeyBaseModel
from pydantic import Field

from common.types import SocketAddress

from . import AgentID, MachineID


class Agent(MutableInfectionMonkeyBaseModel):
    """Represents an agent that has run on a victim machine"""

    id: AgentID = Field(..., frozen=True)
    """Uniquely identifies an instance of an agent"""

    machine_id: MachineID = Field(..., frozen=True)
    """The machine that the agent ran on"""

    registration_time: datetime = Field(frozen=True, default_factory=datetime.now)
    """The time the agent registered with the island"""

    start_time: datetime = Field(..., frozen=True)
    """The time the agent process started"""

    stop_time: Optional[datetime] = Field(default=None)
    """The time the agent process exited"""

    parent_id: Optional[AgentID] = Field(frozen=True, default=None)
    """The ID of the parent agent that spawned this agent"""

    cc_server: Optional[SocketAddress] = Field(default=None)
    """The address that the agent used to communicate with the island"""

    sha256: str = Field(frozen=True, pattern="^[0-9a-fA-F]{64}$")
    """The SHA256 hash of the agent binary"""
