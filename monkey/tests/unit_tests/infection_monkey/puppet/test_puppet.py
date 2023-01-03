import threading
from unittest.mock import MagicMock

import pytest

from common.agent_plugins import AgentPluginType
from common.event_queue import IAgentEventQueue
from infection_monkey.i_puppet import PingScanData
from infection_monkey.puppet import PluginRegistry
from infection_monkey.puppet.puppet import EMPTY_FINGERPRINT, Puppet


@pytest.fixture
def mock_plugin_registry() -> PluginRegistry:
    return PluginRegistry(MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock())


def test_puppet_run_payload_success(mock_plugin_registry):
    p = Puppet(
        agent_event_queue=MagicMock(spec=IAgentEventQueue),
        plugin_registry=mock_plugin_registry,
    )

    payload = MagicMock()
    payload_name = "PayloadOne"

    p.load_plugin(AgentPluginType.PAYLOAD, payload_name, payload)
    p.run_payload(payload_name, {}, threading.Event())

    payload.run.assert_called_once()


def test_puppet_run_multiple_payloads(mock_plugin_registry):
    p = Puppet(
        agent_event_queue=MagicMock(spec=IAgentEventQueue),
        plugin_registry=mock_plugin_registry,
    )

    payload_1 = MagicMock()
    payload1_name = "PayloadOne"

    payload_2 = MagicMock()
    payload2_name = "PayloadTwo"

    payload_3 = MagicMock()
    payload3_name = "PayloadThree"

    p.load_plugin(AgentPluginType.PAYLOAD, payload1_name, payload_1)
    p.load_plugin(AgentPluginType.PAYLOAD, payload2_name, payload_2)
    p.load_plugin(AgentPluginType.PAYLOAD, payload3_name, payload_3)

    p.run_payload(payload1_name, {}, threading.Event())
    payload_1.run.assert_called_once()

    p.run_payload(payload2_name, {}, threading.Event())
    payload_2.run.assert_called_once()

    p.run_payload(payload3_name, {}, threading.Event())
    payload_3.run.assert_called_once()


def test_fingerprint_exception_handling(monkeypatch, mock_plugin_registry):
    p = Puppet(
        agent_event_queue=MagicMock(spec=IAgentEventQueue),
        plugin_registry=mock_plugin_registry,
    )
    p._plugin_registry.get_plugin = MagicMock(side_effect=Exception)
    assert (
        p.fingerprint("", "", PingScanData(response_received=False, os="windows"), {}, {})
        == EMPTY_FINGERPRINT
    )
