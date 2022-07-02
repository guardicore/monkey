from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from marshmallow import Schema, post_load
from marshmallow_enum import EnumField


class IslandMode(Enum):
    UNSET = "unset"
    RANSOMWARE = "ransomware"
    ADVANCED = "advanced"


@dataclass(frozen=True)
class Simulation:
    mode: IslandMode = IslandMode.UNSET


class SimulationSchema(Schema):
    mode = EnumField(IslandMode)

    @post_load
    def _make_simulation(self, data, **kwargs):
        return Simulation(**data)
