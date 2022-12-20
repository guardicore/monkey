import time
from unittest.mock import MagicMock

import pytest

from infection_monkey.master import AutomatedMaster
from infection_monkey.master.control_channel import IslandCommunicationError

INTERVAL = 0.001


def test_terminate_without_start():
    m = AutomatedMaster(None, [], None, MagicMock(), [], MagicMock())

    # Test that call to terminate does not raise exception
    m.terminate()


def test_stop_if_cant_get_config_from_island(monkeypatch):
    cc = MagicMock()
    cc.should_agent_stop = MagicMock(return_value=False)
    cc.get_config = MagicMock(
        side_effect=IslandCommunicationError("Failed to communicate with island")
    )

    monkeypatch.setattr(
        "infection_monkey.master.automated_master.CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC",
        INTERVAL,
    )
    monkeypatch.setattr(
        "infection_monkey.master.automated_master.CHECK_FOR_TERMINATE_INTERVAL_SEC", INTERVAL
    )
    m = AutomatedMaster(None, [], None, cc, [], MagicMock())
    m.start()


@pytest.fixture
def sleep_and_return_config(default_agent_configuration):
    # Ensure that should_agent_stop times out before get_config() returns to prevent the
    # Propagator's sub-threads from hanging
    get_config_sleep_time = INTERVAL * (10)

    def _inner():
        time.sleep(get_config_sleep_time)
        return default_agent_configuration

    return _inner


# NOTE: This test is a little bit brittle, and probably needs too much knowlegde of the internals
#       of AutomatedMaster. For now, it works and it runs quickly. In the future, if we find that
#       this test isn't valuable or it starts causing issues, we can just remove it.
def test_stop_if_cant_get_stop_signal_from_island(monkeypatch, sleep_and_return_config):
    cc = MagicMock()
    cc.should_agent_stop = MagicMock(
        side_effect=IslandCommunicationError("Failed to communicate with island")
    )
    cc.get_config = MagicMock(
        side_effect=sleep_and_return_config,
    )

    monkeypatch.setattr(
        "infection_monkey.master.automated_master.CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC",
        INTERVAL,
    )
    monkeypatch.setattr(
        "infection_monkey.master.automated_master.CHECK_FOR_TERMINATE_INTERVAL_SEC", INTERVAL
    )

    m = AutomatedMaster(None, [], None, cc, [], MagicMock())
    m.start()
