from monkey_island.cc.models.island_mode_model import IslandMode
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum


def set_mode(mode: IslandModeEnum):
    island_mode_model = IslandMode()
    island_mode_model.mode = mode.value
    island_mode_model.save()
    ConfigService.update_config_on_mode_set(mode.value)
