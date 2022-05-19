from abc import ABC
from typing import Optional, Sequence

from monkey_island.cc.models.zero_trust.event import Event


class IEventRepository(ABC):
    def get_events(self, finding_id: Optional[str] = None) -> Sequence[Event]:
        pass

    # Events are saved in IFindingRepository, because finding had many events
