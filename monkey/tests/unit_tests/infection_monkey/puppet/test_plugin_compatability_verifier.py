from copy import deepcopy
from ipaddress import IPv4Address
from unittest.mock import MagicMock

import pytest
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import (
    FAKE_LINK,
    FAKE_MANIFEST_OBJECT,
    FAKE_NAME,
    FAKE_NAME2,
    FAKE_TYPE,
)

from common import OperatingSystem
from common.agent_plugins.agent_plugin_manifest import AgentPluginManifest
from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIError
from infection_monkey.model import TargetHost
from infection_monkey.puppet import PluginCompatabilityVerifier

FAKE_NAME3 = "BogusExploiter"

FAKE_MANIFEST_OBJECT_2 = AgentPluginManifest(
    name=FAKE_NAME2,
    plugin_type=FAKE_TYPE,
    supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
    target_operating_systems=(OperatingSystem.WINDOWS,),
    title="Some exploiter title",
    version="1.0.0",
    link_to_documentation=FAKE_LINK,
)

FAKE_HARD_CODED_PLUGIN_MANIFESTS = {
    FAKE_NAME: FAKE_MANIFEST_OBJECT,
    FAKE_NAME2: FAKE_MANIFEST_OBJECT_2,
}


@pytest.fixture
def island_api_client():
    return MagicMock(spec=IIslandAPIClient)


@pytest.fixture
def plugin_compatability_verifier(island_api_client):
    return PluginCompatabilityVerifier(
        island_api_client, deepcopy(FAKE_HARD_CODED_PLUGIN_MANIFESTS)
    )


@pytest.mark.parametrize(
    "target_host_os, exploiter_name",
    [(None, FAKE_NAME), (OperatingSystem.WINDOWS, FAKE_NAME2), (OperatingSystem.LINUX, FAKE_NAME)],
)
def test_os_compatability_verifier__hard_coded_exploiters(
    target_host_os, exploiter_name, island_api_client, plugin_compatability_verifier
):
    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=target_host_os)

    assert plugin_compatability_verifier.verify_exploiter_compatibility(exploiter_name, target_host)


@pytest.mark.parametrize(
    "target_host_os, exploiter_name",
    [(OperatingSystem.WINDOWS, FAKE_NAME), (OperatingSystem.LINUX, FAKE_NAME2)],
)
def test_os_compatability_verifier__incompatable(
    target_host_os, exploiter_name, island_api_client, plugin_compatability_verifier
):
    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=target_host_os)

    assert not plugin_compatability_verifier.verify_exploiter_compatibility(
        exploiter_name, target_host
    )


@pytest.mark.parametrize("target_host_os", [None, OperatingSystem.LINUX])
def test_os_compatability_verifier__island_api_client(
    target_host_os, island_api_client, plugin_compatability_verifier
):
    island_api_client.get_agent_plugin_manifest = lambda _, __: FAKE_MANIFEST_OBJECT

    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=target_host_os)

    assert plugin_compatability_verifier.verify_exploiter_compatibility(FAKE_NAME3, target_host)


def test_os_compatability_verifier__island_api_client_incompatable(
    island_api_client, plugin_compatability_verifier
):
    island_api_client.get_agent_plugin_manifest = lambda _, __: FAKE_MANIFEST_OBJECT

    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=OperatingSystem.WINDOWS)

    assert not plugin_compatability_verifier.verify_exploiter_compatibility(FAKE_NAME3, target_host)


@pytest.mark.parametrize("target_host_os", [None, OperatingSystem.LINUX])
def test_os_compatability_verifier__island_api_client_error(
    target_host_os, island_api_client, plugin_compatability_verifier
):
    def raise_island_api_error(plugin_type, name):
        raise IslandAPIError

    island_api_client.get_agent_plugin_manifest = raise_island_api_error

    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=target_host_os)
    assert not plugin_compatability_verifier.verify_exploiter_compatibility(FAKE_NAME3, target_host)
