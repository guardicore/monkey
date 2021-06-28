import time

import pytest

from infection_monkey.telemetry.base_telem import BaseTelem
from infection_monkey.telemetry.batchable_telem_mixin import BatchableTelemMixin
from infection_monkey.telemetry.i_batchable_telem import IBatchableTelem
from infection_monkey.telemetry.messengers.batched_telemetry_messenger import (
    BatchedTelemetryMessenger,
)

PERIOD = 0.001


def release_GIL():
    time.sleep(PERIOD)


def advance_clock_to_next_period(monkeypatch):
    patch_time(monkeypatch, time.time() + (PERIOD * 1.01))


def patch_time(monkeypatch, new_time: float):
    monkeypatch.setattr(time, "time", lambda: new_time)


class NonBatchableTelemStub(BaseTelem):
    telem_category = "NonBatchableTelemStub"

    def send(self, log_data=True):
        raise NotImplementedError

    def get_data(self) -> dict:
        return {"1": {"i": "a", "ii": "b"}}

    def __eq__(self, other):
        return self.get_data() == other.get_data() and self.telem_category == other.telem_category


class BatchableTelemStub(BatchableTelemMixin, BaseTelem, IBatchableTelem):
    def __init__(self, value, telem_category="cat1"):
        self._telemetry_entries.append(value)
        self._telem_category = telem_category

    @property
    def telem_category(self):
        return self._telem_category

    def send(self, log_data=True):
        raise NotImplementedError

    def get_data(self) -> dict:
        return {"entries": self._telemetry_entries}


@pytest.fixture
def batched_telemetry_messenger(monkeypatch, telemetry_messenger_spy):
    patch_time(monkeypatch, 0)
    btm = BatchedTelemetryMessenger(telemetry_messenger_spy, period=0.001)
    yield btm

    btm.stop()


def test_send_immediately(batched_telemetry_messenger, telemetry_messenger_spy):
    telem = NonBatchableTelemStub()

    batched_telemetry_messenger.send_telemetry(telem)
    release_GIL()

    assert len(telemetry_messenger_spy.telemetries) == 1
    assert telemetry_messenger_spy.telemetries[0] == telem


def test_send_telem_batch(monkeypatch, batched_telemetry_messenger, telemetry_messenger_spy):
    expected_data = {"entries": [1, 2]}
    telem1 = BatchableTelemStub(1)
    telem2 = BatchableTelemStub(2)

    batched_telemetry_messenger.send_telemetry(telem1)
    batched_telemetry_messenger.send_telemetry(telem2)
    release_GIL()

    assert len(telemetry_messenger_spy.telemetries) == 0
    advance_clock_to_next_period(monkeypatch)
    release_GIL()

    assert len(telemetry_messenger_spy.telemetries) == 1
    assert telemetry_messenger_spy.telemetries[0].get_data() == expected_data


def test_send_different_telem_types(
    monkeypatch, batched_telemetry_messenger, telemetry_messenger_spy
):
    telem1 = BatchableTelemStub(1, "cat1")
    telem2 = BatchableTelemStub(2, "cat2")

    batched_telemetry_messenger.send_telemetry(telem1)
    batched_telemetry_messenger.send_telemetry(telem2)
    release_GIL()

    assert len(telemetry_messenger_spy.telemetries) == 0
    advance_clock_to_next_period(monkeypatch)
    release_GIL()

    assert len(telemetry_messenger_spy.telemetries) == 2
    assert telemetry_messenger_spy.telemetries[0] == telem1
    assert telemetry_messenger_spy.telemetries[1] == telem2


def test_send_two_batches(monkeypatch, batched_telemetry_messenger, telemetry_messenger_spy):
    telem1 = BatchableTelemStub(1, "cat1")
    telem2 = BatchableTelemStub(2, "cat1")

    batched_telemetry_messenger.send_telemetry(telem1)
    advance_clock_to_next_period(monkeypatch)
    release_GIL()

    batched_telemetry_messenger.send_telemetry(telem2)
    release_GIL()
    assert len(telemetry_messenger_spy.telemetries) == 1

    advance_clock_to_next_period(monkeypatch)
    release_GIL()

    assert len(telemetry_messenger_spy.telemetries) == 2
    assert telemetry_messenger_spy.telemetries[1] == telem2
