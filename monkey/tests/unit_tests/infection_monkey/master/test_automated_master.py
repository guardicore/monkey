import time
from unittest.mock import MagicMock

import pytest

from infection_monkey.i_puppet import IPuppet
from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIError
from infection_monkey.master import AutomatedMaster

INTERVAL = 0.001


def test_terminate_without_start():
    m = AutomatedMaster(None, MagicMock(spec=IPuppet), MagicMock(), [])

    # Test that call to terminate does not raise exception
    m.terminate()


def test_stop_if_cant_get_config_from_island(monkeypatch):
    island_api_client = MagicMock(spec=IIslandAPIClient)
    island_api_client.get_config = MagicMock(
        side_effect=IslandAPIError("Failed to communicate with island")
    )
    island_api_client.terminate_signal_is_set = MagicMock(return_value=False)

    monkeypatch.setattr(
        "infection_monkey.master.automated_master.CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC",
        INTERVAL,
    )
    monkeypatch.setattr(
        "infection_monkey.master.automated_master.CHECK_FOR_TERMINATE_INTERVAL_SEC", INTERVAL
    )

    m = AutomatedMaster(None, MagicMock(spec=IPuppet), island_api_client, [])
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
    island_api_client = MagicMock(spec=IIslandAPIClient)
    island_api_client.get_config = MagicMock(
        side_effect=sleep_and_return_config,
    )
    island_api_client.terminate_signal_is_set.side_effect = IslandAPIError(
        "Failed to communicate with island"
    )

    monkeypatch.setattr(
        "infection_monkey.master.automated_master.CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC",
        INTERVAL,
    )
    monkeypatch.setattr(
        "infection_monkey.master.automated_master.CHECK_FOR_TERMINATE_INTERVAL_SEC", INTERVAL
    )

    m = AutomatedMaster(None, MagicMock(spec=IPuppet), island_api_client, [])
    m.start()
