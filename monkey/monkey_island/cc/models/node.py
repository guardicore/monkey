from typing import Mapping, Tuple, TypeAlias

from pydantic import Field, validator

from common.base_models import MutableInfectionMonkeyBaseModel

from . import CommunicationType, MachineID

NodeConnections: TypeAlias = Mapping[MachineID, Tuple[CommunicationType, ...]]


class Node(MutableInfectionMonkeyBaseModel):
    machine_id: MachineID = Field(..., allow_mutation=False)
    connections: NodeConnections
