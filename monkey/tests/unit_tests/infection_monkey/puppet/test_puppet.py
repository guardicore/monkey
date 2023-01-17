import threading
from copy import deepcopy
from unittest.mock import MagicMock

import pytest
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_NAME, FAKE_NAME2
from tests.unit_tests.infection_monkey.puppet.test_plugin_compatability_verifier import (
    FAKE_HARD_CODED_PLUGIN_MANIFESTS,
)

from common import OperatingSystem
from common.agent_plugins import AgentPluginType
from common.event_queue import IAgentEventQueue
from infection_monkey.i_puppet import IncompatibleOperatingSystemError, PingScanData
from infection_monkey.island_api_client import IIslandAPIClient
from infection_monkey.model import TargetHost
from infection_monkey.puppet import PluginCompatabilityVerifier, PluginRegistry
from infection_monkey.puppet.puppet import EMPTY_FINGERPRINT, Puppet


@pytest.fixture
def mock_plugin_registry() -> PluginRegistry:
    return PluginRegistry(
        MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )


@pytest.fixture
def plugin_compatability_verifier() -> PluginCompatabilityVerifier:
    return PluginCompatabilityVerifier(
        MagicMock(spec=IIslandAPIClient), deepcopy(FAKE_HARD_CODED_PLUGIN_MANIFESTS)
    )


def test_puppet_run_payload_success(mock_plugin_registry):
    p = Puppet(
        agent_event_queue=MagicMock(spec=IAgentEventQueue),
        plugin_registry=mock_plugin_registry,
        plugin_compatability_verifier=MagicMock(),
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
        plugin_compatability_verifier=MagicMock(),
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
        plugin_compatability_verifier=MagicMock(),
    )
    p._plugin_registry.get_plugin = MagicMock(side_effect=Exception)
    assert (
        p.fingerprint("", "", PingScanData(response_received=False, os="windows"), {}, {})
        == EMPTY_FINGERPRINT
    )


@pytest.mark.parametrize(
    "target_host_os, exploiter_name",
    [(None, FAKE_NAME), (OperatingSystem.LINUX, FAKE_NAME), (OperatingSystem.WINDOWS, FAKE_NAME2)],
)
def test_exploit_host(
    target_host_os, exploiter_name, mock_plugin_registry, plugin_compatability_verifier
):
    p = Puppet(
        agent_event_queue=MagicMock(spec=IAgentEventQueue),
        plugin_registry=mock_plugin_registry,
        plugin_compatability_verifier=plugin_compatability_verifier,
    )

    exploiter_object = MagicMock()
    p.load_plugin(AgentPluginType.EXPLOITER, exploiter_name, exploiter_object)

    p.exploit_host(
        name=exploiter_name,
        host=TargetHost(ip="1.1.1.1", operating_system=target_host_os),
        current_depth=1,
        servers=[],
        options={},
        interrupt=None,
    )

    exploiter_object.run.assert_called_once()


@pytest.mark.parametrize(
    "target_host_os, exploiter_name",
    [(OperatingSystem.WINDOWS, FAKE_NAME), (OperatingSystem.LINUX, FAKE_NAME2)],
)
def test_exploit_host__incompatable(
    target_host_os, exploiter_name, mock_plugin_registry, plugin_compatability_verifier
):
    p = Puppet(
        agent_event_queue=MagicMock(spec=IAgentEventQueue),
        plugin_registry=mock_plugin_registry,
        plugin_compatability_verifier=plugin_compatability_verifier,
    )

    p.load_plugin(AgentPluginType.EXPLOITER, exploiter_name, MagicMock())

    with pytest.raises(IncompatibleOperatingSystemError):
        p.exploit_host(
            name=exploiter_name,
            host=TargetHost(ip="1.1.1.1", operating_system=target_host_os),
            current_depth=1,
            servers=[],
            options={},
            interrupt=None,
        )
