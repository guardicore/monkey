from typing import Iterable

from infection_monkey.telemetry.i_batchable_telem import IBatchableTelem


class BatchableTelemMixin:
    """
    Implements the IBatchableTelem interface methods using a list.
    """

    @property
    def _telemetry_entries(self):
        if not hasattr(self, "_list"):
            self._list = []

        return self._list

    def get_telemetry_entries(self) -> Iterable:
        return self._telemetry_entries

    def add_telemetry_to_batch(self, telemetry: IBatchableTelem):
        self._telemetry_entries.extend(telemetry.get_telemetry_entries())
