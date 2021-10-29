from monkey_island.cc.models.island_mode_model import IslandMode
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum


def set_mode(mode: IslandModeEnum):
    island_mode_model = IslandMode()
    island_mode_model.mode = mode.value
    island_mode_model.save()


def get_mode() -> str:
    if IslandMode.objects:
        mode = IslandMode.objects[0].mode
        return mode
    else:
        raise ModeNotSetError


class ModeNotSetError(Exception):
    """
    Throw this exception when island mode is not set.
    """
