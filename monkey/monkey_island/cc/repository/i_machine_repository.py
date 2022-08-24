from abc import ABC
from typing import Optional, Sequence

from monkey_island.cc.models import Machine


class IMachineRepository(ABC):
    def save_machine(self, machine: Machine):
        pass

    # TODO define or re-use machine state.
    def get_machines(
        self,
        id: Optional[str] = None,
        ips: Optional[Sequence[str]] = None,
        state: Optional[MachineState] = None,  # noqa: F821
        is_island: Optional[bool] = None,
    ) -> Sequence[Machine]:
        pass
