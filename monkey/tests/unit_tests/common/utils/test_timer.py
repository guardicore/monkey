import time

import pytest

from common.utils import Timer


@pytest.fixture
def start_time(set_current_time):
    start_time = 100
    set_current_time(start_time)

    return start_time


@pytest.fixture
def set_current_time(monkeypatch):
    def inner(current_time):
        monkeypatch.setattr(time, "time", lambda: current_time)

    return inner


@pytest.mark.parametrize(("timeout"), [5, 1.25])
def test_timer_not_expired(start_time, set_current_time, timeout):
    t = Timer()
    t.set(timeout)

    assert not t.is_expired()

    set_current_time(start_time + (timeout - 0.001))
    assert not t.is_expired()


@pytest.mark.parametrize(("timeout"), [5, 1.25])
def test_timer_expired(start_time, set_current_time, timeout):
    t = Timer()
    t.set(timeout)

    assert not t.is_expired()

    set_current_time(start_time + timeout)
    assert t.is_expired()

    set_current_time(start_time + timeout + 0.001)
    assert t.is_expired()


def test_unset_timer_expired():
    t = Timer()

    assert t.is_expired()


@pytest.mark.parametrize(("timeout"), [5, 1.25])
def test_timer_reset(start_time, set_current_time, timeout):
    t = Timer()
    t.set(timeout)

    assert not t.is_expired()

    set_current_time(start_time + timeout)
    assert t.is_expired()

    t.reset()
    assert not t.is_expired()

    set_current_time(start_time + (2 * timeout))
    assert t.is_expired()


def test_time_remaining(start_time, set_current_time):
    timeout = 5

    t = Timer()
    t.set(timeout)

    assert t.time_remaining == timeout

    set_current_time(start_time + 2)
    assert t.time_remaining == 3


def test_time_remaining_is_zero(start_time, set_current_time):
    timeout = 5

    t = Timer()
    t.set(timeout)

    set_current_time(start_time + timeout)
    assert t.time_remaining == 0

    set_current_time(start_time + (2 * timeout))
    assert t.time_remaining == 0
