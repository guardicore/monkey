from monkey_island.cc.models.island_mode_model import IslandMode
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum


def set_mode(mode: IslandModeEnum):
    IslandMode.drop_collection()
    island_mode_model = IslandMode()
    island_mode_model.mode = mode.value
    island_mode_model.save()


def get_mode() -> str:
    if IslandMode.objects:
        mode = IslandMode.objects[0].mode
        return mode
    else:
        return IslandModeEnum.UNSET.value
