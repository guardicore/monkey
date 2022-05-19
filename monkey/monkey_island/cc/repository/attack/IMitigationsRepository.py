from abc import ABC
from typing import Optional

from monkey_island.cc.models.attack.attack_mitigations import AttackMitigations


class IMitigationsRepository(ABC):
    def get_mitigations(self, technique_id: Optional[str] = None) -> AttackMitigations:
        pass

    def save_mitigations(self, mitigations: AttackMitigations):
        pass
