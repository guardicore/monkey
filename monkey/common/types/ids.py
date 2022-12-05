from uuid import UUID

from pydantic import PositiveInt
from typing_extensions import TypeAlias

AgentID: TypeAlias = UUID
HardwareID: TypeAlias = PositiveInt
MachineID: TypeAlias = PositiveInt
