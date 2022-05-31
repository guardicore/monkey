from abc import ABC
from typing import Optional, Sequence


class ILogRepository(ABC):
    # Define log object
    def get_logs(self, agent_id: Optional[str] = None) -> Sequence[Log]:  # noqa: F821
        pass

    def save_log(self, log: Log):  # noqa: F821
        pass

    def delete_log(self, agent_id: str):
        pass
