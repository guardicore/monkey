from typing import TypeAlias
from uuid import UUID

from pydantic import PositiveInt

AgentID: TypeAlias = UUID
HardwareID: TypeAlias = PositiveInt
MachineID: TypeAlias = PositiveInt
