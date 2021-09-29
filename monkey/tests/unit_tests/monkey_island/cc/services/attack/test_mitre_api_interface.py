import json
from pathlib import Path

from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH


def test_get_all_mitigations():
    attack_mitigation_path = (
        Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "setup" / "mongo" / "attack_mitigations.json"
    )

    with open(attack_mitigation_path) as mitigations:
        mitigations = json.load(mitigations)
        assert len(mitigations) >= 266
        mitigation = next(iter(mitigations))["mitigations"][0]
        assert mitigation["name"] is not None
        assert mitigation["description"] is not None
        assert mitigation["url"] is not None
