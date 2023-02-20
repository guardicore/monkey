import threading
from typing import Optional
from unittest.mock import MagicMock

import pytest
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_NAME, FAKE_NAME2

from common import OperatingSystem
from common.agent_plugins import AgentPluginType
from common.event_queue import IAgentEventQueue
from infection_monkey.i_puppet import IncompatibleOperatingSystemError, PingScanData, TargetHost
from infection_monkey.puppet import PluginCompatabilityVerifier, PluginRegistry
from infection_monkey.puppet.puppet import EMPTY_FINGERPRINT, Puppet


@pytest.fixture
def mock_agent_event_queue() -> IAgentEventQueue:
    return MagicMock(spec=IAgentEventQueue)


@pytest.fixture
def mock_plugin_registry() -> PluginRegistry:
    return PluginRegistry(
        OperatingSystem.WINDOWS,
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )


@pytest.fixture
def mock_plugin_compatability_verifier() -> PluginCompatabilityVerifier:
    pcv = MagicMock(spec=PluginCompatabilityVerifier)
    pcv.verify_exploiter_compatibility = MagicMock(return_value=True)

    return pcv


@pytest.fixture
def puppet(
    mock_agent_event_queue: IAgentEventQueue,
    mock_plugin_registry: PluginRegistry,
    mock_plugin_compatability_verifier: PluginCompatabilityVerifier,
) -> Puppet:
    return Puppet(
        agent_event_queue=mock_agent_event_queue,
        plugin_registry=mock_plugin_registry,
        plugin_compatability_verifier=mock_plugin_compatability_verifier,
    )


def test_puppet_run_payload_success(puppet: Puppet):
    payload = MagicMock()
    payload_name = "PayloadOne"

    puppet.load_plugin(AgentPluginType.PAYLOAD, payload_name, payload)
    puppet.run_payload(payload_name, {}, threading.Event())

    payload.run.assert_called_once()


def test_puppet_run_multiple_payloads(puppet: Puppet):
    payload_1 = MagicMock()
    payload1_name = "PayloadOne"

    payload_2 = MagicMock()
    payload2_name = "PayloadTwo"

    payload_3 = MagicMock()
    payload3_name = "PayloadThree"

    puppet.load_plugin(AgentPluginType.PAYLOAD, payload1_name, payload_1)
    puppet.load_plugin(AgentPluginType.PAYLOAD, payload2_name, payload_2)
    puppet.load_plugin(AgentPluginType.PAYLOAD, payload3_name, payload_3)

    puppet.run_payload(payload1_name, {}, threading.Event())
    payload_1.run.assert_called_once()

    puppet.run_payload(payload2_name, {}, threading.Event())
    payload_2.run.assert_called_once()

    puppet.run_payload(payload3_name, {}, threading.Event())
    payload_3.run.assert_called_once()


def test_fingerprint_exception_handling(puppet: Puppet, mock_plugin_registry: PluginRegistry):
    mock_plugin_registry.get_plugin = MagicMock(side_effect=Exception)  # type: ignore [assignment]
    assert (
        puppet.fingerprint("", "", PingScanData(response_received=False, os="windows"), {}, {})
        == EMPTY_FINGERPRINT
    )


@pytest.mark.parametrize(
    "target_host_os, exploiter_name",
    [(None, FAKE_NAME), (OperatingSystem.LINUX, FAKE_NAME), (OperatingSystem.WINDOWS, FAKE_NAME2)],
)
def test_exploit_host(
    target_host_os: Optional[OperatingSystem],
    exploiter_name: str,
    puppet: Puppet,
):
    exploiter_object = MagicMock()
    puppet.load_plugin(AgentPluginType.EXPLOITER, exploiter_name, exploiter_object)

    puppet.exploit_host(
        name=exploiter_name,
        host=TargetHost(ip="1.1.1.1", operating_system=target_host_os),
        current_depth=1,
        servers=[],
        options={},
        interrupt=threading.Event(),
    )

    exploiter_object.run.assert_called_once()


@pytest.mark.parametrize(
    "target_host_os, exploiter_name",
    [(OperatingSystem.WINDOWS, FAKE_NAME), (OperatingSystem.LINUX, FAKE_NAME2)],
)
def test_exploit_host__incompatable(
    target_host_os: Optional[OperatingSystem],
    exploiter_name: str,
    puppet: Puppet,
    mock_plugin_compatability_verifier: PluginCompatabilityVerifier,
):
    mock_plugin_compatability_verifier.verify_exploiter_compatibility = MagicMock(  # type: ignore [assignment]  # noqa: E501
        return_value=False
    )

    with pytest.raises(IncompatibleOperatingSystemError):
        puppet.exploit_host(
            name=exploiter_name,
            host=TargetHost(ip="1.1.1.1", operating_system=target_host_os),
            current_depth=1,
            servers=[],
            options={},
            interrupt=threading.Event(),
        )
