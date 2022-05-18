from abc import ABC
from typing import Optional, Sequence


class IMachineRepository(ABC):
    # TODO define Machine object(ORM model)
    def save_machine(self, machine: Machine):
        pass

    # TODO define Machine object(ORM model)
    # TODO define or re-use machine state.
    def get_machines(
        self,
        id: Optional[str] = None,
        ips: Optional[Sequence[str]] = None,
        state: Optional[MachineState] = None,
        is_island: Optional[bool] = None,
    ) -> Sequence[Machine]:
        pass
