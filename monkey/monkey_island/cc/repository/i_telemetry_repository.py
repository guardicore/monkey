from abc import ABC
from typing import Optional, Sequence

from monkey_island.cc.models.telemetries.telemetry import Telemetry


class ITelemetryRepository(ABC):
    def save_telemetry(self, telemetry: Telemetry):
        pass

    # TODO define all telemetry types
    # Potentially we'll need to define each telem type separately. As it stands there's no way to
    # get exploit telemetries by exploiter for example
    def get_telemetries(
        self,
        id: Optional[str] = None,
        type: Optional[TelemetryType] = None,  # noqa: F821
        monkey_id: Optional[str] = None,
    ) -> Sequence[Telemetry]:
        pass
