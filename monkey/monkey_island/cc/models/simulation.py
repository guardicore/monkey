from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from marshmallow import Schema, post_load
from marshmallow_enum import EnumField


class IslandModeEnum(Enum):
    UNSET = "unset"
    RANSOMWARE = "ransomware"
    ADVANCED = "advanced"


@dataclass(frozen=True)
class Simulation:
    mode: IslandModeEnum = IslandModeEnum.UNSET


class SimulationSchema(Schema):
    mode = EnumField(IslandModeEnum)

    @post_load
    def _make_simulation(self, data, **kwargs):
        return Simulation(**data)
