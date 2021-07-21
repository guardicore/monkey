from typing import Dict

import dpath.util

import monkey_island.cc.services.config as config_service
from monkey_island.cc.services.config_manipulators import MANIPULATOR_PER_MODE
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum


def update_config_on_mode_set(mode: IslandModeEnum) -> bool:
    config = config_service.ConfigService.get_config()
    return update_config_per_mode(mode.value, config, True)


def update_config_per_mode(mode: str, config: Dict, should_encrypt: bool) -> bool:
    config = _set_default_config_values_per_mode(mode, config)
    return config_service.ConfigService.update_config(
        config_json=config, should_encrypt=should_encrypt
    )


def _set_default_config_values_per_mode(mode: str, config: Dict) -> Dict:
    config_manipulator = MANIPULATOR_PER_MODE[mode]
    config = _apply_config_manipulator(config, config_manipulator)
    return config


def _apply_config_manipulator(config: Dict, config_manipulator: Dict):
    for path, value in config_manipulator.items():
        dpath.util.set(config, path, value, ".")
    return config
