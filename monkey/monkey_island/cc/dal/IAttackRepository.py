from abc import ABC
from typing import Sequence

from monkey_island.cc.models.attack import Mitigation


class IRepository(ABC):
    # Att&ck just add not implemented raises
    ######################################
    # This will likely stay the same as mitigations are external data
    def save_mitigations(self, mitigations: Sequence[Mitigation]):
        pass

    # This will likely remain if we plan to keep the report actionable
    def get_mitigation_by_technique(self, technique_id: str) -> Mitigation:
        pass

    # This could go away, since attack report is not costly to generate and we'll refactor it
    def save_attack_report(self, attack_report: dict):
        raise NotImplementedError

    # This will probably go away once we use endpoints instead
    def get_attack_report(self):
        raise NotImplementedError
