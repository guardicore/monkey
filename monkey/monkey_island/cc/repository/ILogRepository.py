from abc import ABC
from typing import Optional, Sequence


class ILogRepository(ABC):
    # Define log object
    def get_logs(self, agent_id: Optional[str] = None) -> Sequence[Log]:
        pass

    def save_log(self, log: Log):
        pass

    def delete_log(self, agent_id: str):
        pass
