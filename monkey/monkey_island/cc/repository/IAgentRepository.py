from abc import ABC
from typing import Optional, Sequence

from monkey_island.cc.models import Monkey


class IAgentRepository(ABC):
    # TODO rename Monkey document to Agent
    def save_agent(self, agent: Monkey):
        pass

    def get_agents(
        self, id: Optional[str] = None, running: Optional[bool] = None
    ) -> Sequence[Monkey]:
        pass
