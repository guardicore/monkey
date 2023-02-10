import time
from unittest.mock import MagicMock

import pytest

from common.utils import Timer
from infection_monkey.utils.decorators import request_cache


class MockTimer(Timer):
    def __init__(self):
        self._time_remaining = 0
        self._set_time = 0

    def set(self, timeout_sec: float):
        self._time_remaining = timeout_sec
        self._set_time = timeout_sec

    def set_expired(self):
        self._time_remaining = 0

    @property
    def time_remaining(self) -> float:
        return self._time_remaining

    def reset(self):
        """
        Reset the timer without changing the timeout
        """
        self._time_remaining = self._set_time


class MockTimerFactory:
    def __init__(self):
        self._instance = None

    def __call__(self):
        if self._instance is None:
            mt = MockTimer()
            self._instance = mt

        return self._instance

    def reset(self):
        self._instance = None


mock_timer_factory = MockTimerFactory()


@pytest.fixture
def mock_timer(monkeypatch):
    mock_timer_factory.reset

    monkeypatch.setattr("infection_monkey.utils.decorators.Timer", mock_timer_factory)

    return mock_timer_factory()


def test_request_cache(mock_timer):
    mock_request = MagicMock(side_effect=lambda: time.perf_counter_ns())

    @request_cache(10)
    def make_request():
        return mock_request()

    t1 = make_request()
    t2 = make_request()

    assert t1 == t2

    mock_timer.set_expired()

    t3 = make_request()
    t4 = make_request()

    assert t3 != t1
    assert t3 == t4
