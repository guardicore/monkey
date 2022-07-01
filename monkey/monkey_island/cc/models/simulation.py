from __future__ import annotations

from dataclasses import dataclass

from marshmallow import Schema, post_load
from marshmallow_enum import EnumField

from monkey_island.cc.services.mode.mode_enum import IslandModeEnum


@dataclass(frozen=True)
class Simulation:
    mode: IslandModeEnum = IslandModeEnum.UNSET


class SimulationSchema(Schema):
    mode = EnumField(IslandModeEnum)

    @post_load
    def _make_simulation(self, data, **kwargs):
        return Simulation(**data)
