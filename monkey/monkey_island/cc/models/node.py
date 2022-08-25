from typing import Sequence, Tuple

from pydantic import Field, validator

from common.base_models import MutableInfectionMonkeyBaseModel
from common.transforms import make_immutable_nested_sequence

from . import CommunicationType, MachineID

ConnectionsSequence = Sequence[Tuple[MachineID, Sequence[CommunicationType]]]


class Node(MutableInfectionMonkeyBaseModel):
    machine_id: MachineID = Field(..., allow_mutation=False)
    connections: ConnectionsSequence

    _make_immutable_nested_sequence = validator("connections", pre=True, allow_reuse=True)(
        make_immutable_nested_sequence
    )
