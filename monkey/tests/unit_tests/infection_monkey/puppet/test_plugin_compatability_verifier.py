from ipaddress import IPv4Address
from unittest.mock import MagicMock

import pytest
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import (
    FAKE_MANIFEST_OBJECT,
    FAKE_NAME,
)

from common import OperatingSystem
from infection_monkey.i_puppet import IncompatibleOperatingSystemError
from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIError
from infection_monkey.model import TargetHost
from infection_monkey.puppet import PluginCompatabilityVerifier


@pytest.fixture
def island_api_client():
    return MagicMock(spec=IIslandAPIClient)


@pytest.fixture
def plugin_compatability_verifier(island_api_client):
    return PluginCompatabilityVerifier(island_api_client)


@pytest.mark.parametrize("target_host_os", [None, OperatingSystem.WINDOWS, OperatingSystem.LINUX])
def test_os_compatability_verifier__hard_coded_exploiters(
    target_host_os, island_api_client, plugin_compatability_verifier
):
    def raise_island_api_error(plugin_type, name):
        raise IslandAPIError

    island_api_client.get_agent_plugin_manifest = raise_island_api_error

    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=target_host_os)

    assert plugin_compatability_verifier.verify_exploiter_compatibility(
        "HadoopExploiter", target_host
    )


@pytest.mark.parametrize(
    "target_host_os, exploiter_name",
    [(OperatingSystem.WINDOWS, "SSHExploiter"), (OperatingSystem.LINUX, "SMBExploiter")],
)
def test_os_compatability_verifier__incompatable_os_error(
    target_host_os, exploiter_name, island_api_client, plugin_compatability_verifier
):
    def raise_island_api_error(plugin_type, name):
        raise IslandAPIError

    island_api_client.get_agent_plugin_manifest = raise_island_api_error

    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=target_host_os)

    with pytest.raises(IncompatibleOperatingSystemError):
        plugin_compatability_verifier.verify_exploiter_compatibility(exploiter_name, target_host)


@pytest.mark.parametrize("target_host_os", [None, OperatingSystem.LINUX])
def test_os_compatability_verifier__island_api_client(
    target_host_os, island_api_client, plugin_compatability_verifier
):
    island_api_client.get_agent_plugin_manifest = lambda _, __: FAKE_MANIFEST_OBJECT

    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=target_host_os)

    assert plugin_compatability_verifier.verify_exploiter_compatibility(FAKE_NAME, target_host)


def test_os_compatability_verifier__island_api_client_incompatable(
    island_api_client, plugin_compatability_verifier
):
    island_api_client.get_agent_plugin_manifest = lambda _, __: FAKE_MANIFEST_OBJECT

    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=OperatingSystem.WINDOWS)

    with pytest.raises(IncompatibleOperatingSystemError):
        plugin_compatability_verifier.verify_exploiter_compatibility(FAKE_NAME, target_host)
