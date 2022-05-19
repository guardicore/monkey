from abc import ABC
from typing import Sequence

from monkey_island.cc.models.exported_telem import ExportedTelem


class ITelemStoreRepository(ABC):
    def get_telemetries(self) -> Sequence[ExportedTelem]:
        pass

    def save_telemetry(self, telemetry: ExportedTelem):
        pass
