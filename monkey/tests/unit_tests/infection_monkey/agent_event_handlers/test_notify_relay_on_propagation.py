from ipaddress import IPv4Address
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from monkeyevents import PropagationEvent

from infection_monkey.agent_event_handlers import notify_relay_on_propagation
from infection_monkey.network.relay import TCPRelay

TARGET_ADDRESS = IPv4Address("192.168.1.10")

SUCCESSFUL_PROPAGATION_EVENT = PropagationEvent(
    source=UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5"),
    target=TARGET_ADDRESS,
    tags=frozenset({"test"}),
    success=True,
    exploiter_name="test_exploiter",
)

FAILED_PROPAGATION_EVENT = PropagationEvent(
    source=UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5"),
    target=TARGET_ADDRESS,
    tags=frozenset({"test"}),
    success=False,
    exploiter_name="test_exploiter",
    error_message="everything is broken",
)


@pytest.fixture
def mock_tcp_relay():
    return MagicMock(spec=TCPRelay)


def test_relay_notified_on_successful_propation(mock_tcp_relay):
    handler = notify_relay_on_propagation(mock_tcp_relay)
    handler(SUCCESSFUL_PROPAGATION_EVENT)

    mock_tcp_relay.add_potential_user.assert_called_once_with(TARGET_ADDRESS)


def test_relay_not_notified_on_successful_propation(mock_tcp_relay):
    handler = notify_relay_on_propagation(mock_tcp_relay)
    handler(FAILED_PROPAGATION_EVENT)

    mock_tcp_relay.add_potential_user.assert_not_called()


def test_handler_doesnt_raise_if_relay_is_none():
    handler = notify_relay_on_propagation(None)

    # Raises AttributeError on failure
    handler(SUCCESSFUL_PROPAGATION_EVENT)
