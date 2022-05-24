from abc import ABC
from typing import Optional

# Zero trust finding
from monkey_island.cc.models.zero_trust.finding import Finding


class IFindingRepository(ABC):
    def get_findings(self, test: Optional[str] = None) -> Finding:
        pass

    def save_finding(self, finding: Finding):
        pass
