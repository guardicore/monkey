import logging

from monkey_island.cc.models.island_mode_model import IslandMode
from monkey_island.cc.services.config_manipulator import update_config_on_mode_set
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum

LOG = logging.getLogger(__name__)


def set_mode(mode: IslandModeEnum):
    island_mode_model = IslandMode()
    island_mode_model.mode = mode.value
    island_mode_model.save()
    if not update_config_on_mode_set(mode):
        LOG.error(
            "Could not apply configuration changes per mode. Using default advanced configuration."
        )
