from monkey_island.cc.services.mode.mode_enum import IslandModeEnum

MANIPULATOR_PER_MODE = {
    IslandModeEnum.ADVANCED.value: {},
    IslandModeEnum.RANSOMWARE.value: {"monkey.post_breach.post_breach_actions": []},
}
