import threading
from typing import Optional
from unittest.mock import MagicMock

import pytest
from monkeytypes import AgentPluginType
from tests.data_for_tests.propagation_credentials import CREDENTIALS
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_NAME, FAKE_NAME2

from common import OperatingSystem
from common.event_queue import IAgentEventQueue
from common.types import AgentID
from infection_monkey.i_puppet import (
    IncompatibleLocalOperatingSystemError,
    IncompatibleTargetOperatingSystemError,
    PingScanData,
    TargetHost,
)
from infection_monkey.puppet import PluginCompatibilityVerifier, PluginRegistry
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
    )


@pytest.fixture
def mock_plugin_compatibility_verifier() -> PluginCompatibilityVerifier:
    pcv = MagicMock(spec=PluginCompatibilityVerifier)
    pcv.verify_target_operating_system_compatibility = MagicMock(return_value=True)
    pcv.verify_local_operating_system_compatibility = MagicMock(return_value=True)  # type: ignore [assignment]  # noqa: E501

    return pcv


@pytest.fixture
def puppet(
    mock_agent_event_queue: IAgentEventQueue,
    mock_plugin_registry: PluginRegistry,
    mock_plugin_compatibility_verifier: PluginCompatibilityVerifier,
) -> Puppet:
    return Puppet(
        agent_event_queue=mock_agent_event_queue,
        plugin_registry=mock_plugin_registry,
        plugin_compatibility_verifier=mock_plugin_compatibility_verifier,
        agent_id=AgentID("4277aa81-660b-4673-b96c-443ed525b4d0"),
    )


def test_run_credentials_collector(puppet: Puppet):
    plugin_name = "cc_1"
    credentials_collector = MagicMock()
    credentials_collector.run = MagicMock(return_value=CREDENTIALS)
    puppet.load_plugin(AgentPluginType.CREDENTIALS_COLLECTOR, plugin_name, credentials_collector)

    collected_credentials = puppet.run_credentials_collector(plugin_name, {}, threading.Event())

    assert collected_credentials == CREDENTIALS


def test_run_credentials_collector__incompatible_local_os(
    mock_plugin_compatibility_verifier: PluginCompatibilityVerifier, puppet: Puppet
):
    mock_plugin_compatibility_verifier.verify_local_operating_system_compatibility = MagicMock(  # type: ignore [assignment]  # noqa: E501
        return_value=False
    )

    with pytest.raises(IncompatibleLocalOperatingSystemError):
        puppet.run_credentials_collector("test", {}, threading.Event())


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


def test_run_payload__incompatible_local_os(
    mock_plugin_compatibility_verifier: PluginCompatibilityVerifier, puppet: Puppet
):
    mock_plugin_compatibility_verifier.verify_local_operating_system_compatibility = MagicMock(  # type: ignore [assignment]  # noqa: E501
        return_value=False
    )

    with pytest.raises(IncompatibleLocalOperatingSystemError):
        puppet.run_payload("test", {}, threading.Event())


def test_fingerprint_exception_handling(puppet: Puppet, mock_plugin_registry: PluginRegistry):
    mock_plugin_registry.get_plugin = MagicMock(side_effect=Exception)  # type: ignore [assignment]
    assert (
        puppet.fingerprint(
            "",
            "",
            PingScanData(response_received=False, os="windows"),
            {},  # type: ignore [arg-type]
            {},  # type: ignore [arg-type]
        )
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
def test_exploit_host__incompatible(
    target_host_os: Optional[OperatingSystem],
    exploiter_name: str,
    puppet: Puppet,
    mock_plugin_compatibility_verifier: PluginCompatibilityVerifier,
):
    mock_plugin_compatibility_verifier.verify_target_operating_system_compatibility = MagicMock(  # type: ignore [assignment]  # noqa: E501
        return_value=False
    )

    with pytest.raises(IncompatibleTargetOperatingSystemError):
        puppet.exploit_host(
            name=exploiter_name,
            host=TargetHost(ip="1.1.1.1", operating_system=target_host_os),
            current_depth=1,
            servers=[],
            options={},
            interrupt=threading.Event(),
        )


def test_malfunctioning_plugin__exploiter(puppet: Puppet):
    malfunctioning_exploiter = MagicMock()
    malfunctioning_exploiter.run = MagicMock(return_value=None)
    puppet.load_plugin(AgentPluginType.EXPLOITER, FAKE_NAME, malfunctioning_exploiter)

    exploiter_result = puppet.exploit_host(
        name=FAKE_NAME,
        host=TargetHost(ip="1.1.1.1", operating_system=OperatingSystem.WINDOWS),
        current_depth=1,
        servers=[],
        options={},
        interrupt=threading.Event(),
    )

    assert exploiter_result.exploitation_success is False
    assert exploiter_result.propagation_success is False
    assert exploiter_result.error_message != ""


def test_exploit_host__incompatible_local_operating_system(
    puppet: Puppet,
    mock_plugin_compatibility_verifier: PluginCompatibilityVerifier,
):
    mock_plugin_compatibility_verifier.verify_local_operating_system_compatibility = MagicMock(  # type: ignore [assignment]  # noqa: E501
        return_value=False
    )

    with pytest.raises(IncompatibleLocalOperatingSystemError):
        puppet.exploit_host(
            name=FAKE_NAME,
            host=TargetHost(ip="1.1.1.1", operating_system=OperatingSystem.WINDOWS),
            current_depth=1,
            servers=[],
            options={},
            interrupt=threading.Event(),
        )
