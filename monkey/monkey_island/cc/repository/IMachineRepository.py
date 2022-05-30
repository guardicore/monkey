from abc import ABC
from typing import Optional, Sequence


class IMachineRepository(ABC):
    # TODO define Machine object(ORM model)
    def save_machine(self, machine: Machine):  # noqa: F821
        pass

    # TODO define Machine object(ORM model)
    # TODO define or re-use machine state.
    # TODO investigate where should the state be stored in edge or both edge and machine
    def get_machines(
        self,
        id: Optional[str] = None,
        ips: Optional[Sequence[str]] = None,
        state: Optional[MachineState] = None,  # noqa: F821
        is_island: Optional[bool] = None,
    ) -> Sequence[Machine]:  # noqa: F821
        pass
