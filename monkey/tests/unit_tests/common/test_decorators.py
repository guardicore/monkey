import time
from unittest.mock import MagicMock

import pytest
from egg_timer import EggTimer

from common.decorators import request_cache


class MockTimer(EggTimer):
    def __init__(self):
        self._timeout_ns = 0
        self._start_time_ns = 0

    def set(self, timeout_sec: float):
        self._timeout_ns = timeout_sec * 1e9
        self._start_time_ns = time.monotonic_ns()

    def set_expired(self):
        self._timeout_ns = 0

    @property
    def time_remaining_sec(self) -> float:
        return self._timeout_ns

    def reset(self):
        """
        Reset the timer without changing the timeout
        """
        self._timeout_ns = self._start_time_ns


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

    monkeypatch.setattr("common.decorators.EggTimer", mock_timer_factory)

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


def test_request_cache__clear_cache(mock_timer):
    mock_request = MagicMock(side_effect=lambda: time.perf_counter_ns())

    @request_cache(10)
    def make_request():
        return mock_request()

    t1 = make_request()
    make_request.clear_cache()
    t2 = make_request()
    assert t1 != t2
