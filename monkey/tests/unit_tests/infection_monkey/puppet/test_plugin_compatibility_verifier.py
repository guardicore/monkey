from ipaddress import IPv4Address
from unittest.mock import MagicMock

import pytest
from monkeytypes import AgentPluginManifest, AgentPluginType, OperatingSystem
from tests.common.fake_manifests import FAKE_MANIFEST_OBJECT, FAKE_NAME, FAKE_NAME2, URL

from infection_monkey.i_puppet import TargetHost
from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIError
from infection_monkey.puppet import PluginCompatibilityVerifier

FAKE_NAME3 = "http://www.BogusExploiter.com"


@pytest.fixture
def island_api_client():
    return MagicMock(spec=IIslandAPIClient)


def raise_island_api_error(plugin_type, name):
    raise IslandAPIError


@pytest.fixture
def plugin_compatibility_verifier(island_api_client):
    return PluginCompatibilityVerifier(island_api_client, OperatingSystem.WINDOWS)


@pytest.mark.parametrize(
    "target_host_os, exploiter_name",
    [(OperatingSystem.WINDOWS, FAKE_NAME), (OperatingSystem.LINUX, FAKE_NAME2)],
)
def test_os_compatibility_verifier__incompatible(
    target_host_os, exploiter_name, island_api_client, plugin_compatibility_verifier
):
    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=target_host_os)

    assert not plugin_compatibility_verifier.verify_target_operating_system_compatibility(
        AgentPluginType.EXPLOITER, exploiter_name, target_host
    )


@pytest.mark.parametrize("target_host_os", [None, OperatingSystem.LINUX])
def test_os_compatibility_verifier__island_api_client(
    target_host_os, island_api_client, plugin_compatibility_verifier
):
    island_api_client.get_agent_plugin_manifest = lambda _, __: FAKE_MANIFEST_OBJECT

    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=target_host_os)

    assert plugin_compatibility_verifier.verify_target_operating_system_compatibility(
        AgentPluginType.EXPLOITER, FAKE_NAME3, target_host
    )


def test_os_compatibility_verifier__island_api_client_incompatible(
    island_api_client, plugin_compatibility_verifier
):
    island_api_client.get_agent_plugin_manifest = lambda _, __: FAKE_MANIFEST_OBJECT

    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=OperatingSystem.WINDOWS)

    assert not plugin_compatibility_verifier.verify_target_operating_system_compatibility(
        AgentPluginType.EXPLOITER, FAKE_NAME3, target_host
    )


@pytest.mark.parametrize("target_host_os", [None, OperatingSystem.LINUX])
def test_os_compatibility_verifier__island_api_client_error(
    target_host_os, island_api_client, plugin_compatibility_verifier
):
    island_api_client.get_agent_plugin_manifest = raise_island_api_error

    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=target_host_os)
    assert not plugin_compatibility_verifier.verify_target_operating_system_compatibility(
        AgentPluginType.EXPLOITER, FAKE_NAME3, target_host
    )


@pytest.mark.parametrize(
    "plugin_type", [AgentPluginType.EXPLOITER, AgentPluginType.CREDENTIALS_COLLECTOR]
)
@pytest.mark.parametrize(
    "operating_system, supported_operating_systems, expected_result",
    [
        (OperatingSystem.LINUX, [OperatingSystem.LINUX], True),
        (OperatingSystem.LINUX, [OperatingSystem.WINDOWS], False),
        (OperatingSystem.LINUX, [OperatingSystem.LINUX, OperatingSystem.WINDOWS], True),
        (OperatingSystem.WINDOWS, [OperatingSystem.LINUX], False),
        (OperatingSystem.WINDOWS, [OperatingSystem.WINDOWS], True),
        (OperatingSystem.WINDOWS, [OperatingSystem.LINUX, OperatingSystem.WINDOWS], True),
    ],
)
def test_verify_local_os_compatibility(
    plugin_type, operating_system, supported_operating_systems, expected_result
):
    manifest = AgentPluginManifest(
        name=FAKE_NAME2,
        plugin_type=plugin_type,
        supported_operating_systems=supported_operating_systems,
        title="Some exploiter title",
        version="1.0.0",
        link_to_documentation=URL,
    )
    island_api_client.get_agent_plugin_manifest = lambda _, __: manifest
    plugin_compatibility_verifier = PluginCompatibilityVerifier(island_api_client, operating_system)

    actual_result = plugin_compatibility_verifier.verify_local_operating_system_compatibility(
        plugin_type, FAKE_NAME2
    )

    assert actual_result is expected_result


def test_local_os_compatibility__island_api_client_error(
    island_api_client, plugin_compatibility_verifier
):
    island_api_client.get_agent_plugin_manifest = raise_island_api_error

    assert not plugin_compatibility_verifier.verify_local_operating_system_compatibility(
        AgentPluginType.EXPLOITER, FAKE_NAME3
    )


@pytest.mark.parametrize(
    "plugin_type", [AgentPluginType.EXPLOITER, AgentPluginType.CREDENTIALS_COLLECTOR]
)
def test_manifest_caching(island_api_client, plugin_type):
    manifest = AgentPluginManifest(
        name=FAKE_NAME2,
        plugin_type=plugin_type,
        supported_operating_systems=[OperatingSystem.LINUX],
        title="Some exploiter title",
        version="1.0.0",
        link_to_documentation=URL,
    )
    island_api_client.get_agent_plugin_manifest.side_effect = lambda _, __: manifest
    plugin_compatibility_verifier = PluginCompatibilityVerifier(
        island_api_client, OperatingSystem.LINUX
    )

    plugin_compatibility_verifier.verify_local_operating_system_compatibility(
        plugin_type, FAKE_NAME2
    )
    plugin_compatibility_verifier.verify_local_operating_system_compatibility(
        plugin_type, FAKE_NAME2
    )

    assert island_api_client.get_agent_plugin_manifest.call_count == 1
