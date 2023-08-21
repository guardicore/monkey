from pathlib import Path
from typing import BinaryIO, Callable
from unittest.mock import MagicMock

import pytest
import requests
import requests_mock
from tests.unit_tests.monkey_island.cc.services.agent_plugin_service.conftest import (
    build_agent_plugin_tar,
)

from common import OperatingSystem
from monkey_island.cc.repositories import RetrievalError
from monkey_island.cc.services.agent_plugin_service.agent_plugin_service import (
    AGENT_PLUGIN_REPOSITORY_URL,
    AgentPluginService,
)
from monkey_island.cc.services.agent_plugin_service.errors import PluginInstallationError
from monkey_island.cc.services.agent_plugin_service.i_agent_plugin_repository import (
    IAgentPluginRepository,
)
from monkey_island.cc.services.agent_plugin_service.i_agent_plugin_service import (
    IAgentPluginService,
)

SSH_EXPLOITER = [
    {
        "name": "SSH",
        "type_": "Exploiter",
        "resource_path": "SSH-exploiter-v1.0.0.tar",
        "sha256": "862d4fd8c9d6c51926d34ac083f75c99d4fe4c3b3052de9e3d5995382a277a43",
        "description": "Attempts a brute-force attack against SSH using known "
        "credentials, including SSH keys.",
        "version": "1.0.0",
        "safe": True,
    }
]

EXPLOITERS = {
    "RDP": [
        {
            "name": "RDP",
            "type_": "Exploiter",
            "resource_path": "RDP-exploiter-v1.0.0.tar",
            "sha256": "09d6afa5bab988157a9f9ab151b63b068749d1708a1e13a6ab76aaefc2e34ff3",
            "description": "Attempts a brute-force attack over RDP using known credentials.",
            "version": "1.0.0",
            "safe": True,
        }
    ],
    "SSH": SSH_EXPLOITER,
}

CREDENTIALS_COLLECTORS = {
    "Mimikatz": [
        {
            "name": "Mimikatz",
            "type_": "Credentials_Collector",
            "resource_path": "Mimikatz-credentials_collector-v1.0.2.tar",
            "sha256": "2999adb179558cff18f6fd4da0b1bdc63093200018a71cb2e1560d197a6314bb",
            "description": "Collects credentials from Windows Credential Manager using Mimikatz.",
            "version": "1.0.2",
            "safe": True,
        }
    ]
}


EXPECTED_SERIALIZED_AGENT_PLUGIN_REPOSITORY_INDEX = {
    "timestamp": 1692629886.4792287,
    "compatible_infection_monkey_version": "development",
    "plugins": {
        "Credentials_Collector": CREDENTIALS_COLLECTORS,
        "Exploiter": EXPLOITERS,
        "Fingerprinter": {},
        "Payload": {},
    },
}

EXPECTED_SERIALIZED_AGENT_PLUGIN_REPOSITORY_SIMPLE_INDEX = {
    "timestamp": 1692629886.4792287,
    "compatible_infection_monkey_version": "development",
    "plugins": {
        "Credentials_Collector": {},
        "Exploiter": {
            "SSH": SSH_EXPLOITER,
        },
        "Fingerprinter": {},
        "Payload": {},
    },
}


@pytest.fixture
def request_mock_instance():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def agent_plugin_repository() -> IAgentPluginRepository:
    return MagicMock(spec=IAgentPluginRepository)


@pytest.fixture
def agent_plugin_repository_index(agent_plugin_repository_index_file):
    with open(agent_plugin_repository_index_file, "r") as f:
        return f.read()


@pytest.fixture
def agent_plugin_repository_index_simple(agent_plugin_repository_index_simple_file):
    with open(agent_plugin_repository_index_simple_file, "r") as f:
        return f.read()


@pytest.fixture
def agent_plugin_service(agent_plugin_repository) -> IAgentPluginService:
    return AgentPluginService(agent_plugin_repository)


@pytest.mark.parametrize(
    "plugin_os, plugin_path",
    [
        (OperatingSystem.WINDOWS, "only-windows-vendor-plugin-source-input.tar"),
        (OperatingSystem.LINUX, "only-linux-vendor-plugin-source-input.tar"),
    ],
)
def test_agent_plugin_service__install_agent_plugin_archive(
    plugin_data_dir: Path,
    plugin_os: OperatingSystem,
    plugin_path: str,
    agent_plugin_repository: IAgentPluginRepository,
    agent_plugin_service: IAgentPluginService,
    build_agent_plugin_tar_with_source_tar: Callable[[Path], BinaryIO],
):
    agent_plugin_tar = build_agent_plugin_tar_with_source_tar(plugin_data_dir / plugin_path)
    agent_plugin_service.install_agent_plugin_archive(agent_plugin_tar.getvalue())

    assert agent_plugin_repository.remove_agent_plugin.call_count == 1

    assert agent_plugin_repository.store_agent_plugin.call_count == 1
    assert agent_plugin_repository.store_agent_plugin.call_args[1]["operating_system"] is plugin_os


@pytest.mark.parametrize(
    "plugin_path_actual",
    ["multi-vendor-plugin-source-input.tar", "cross-platform-plugin-source.tar"],
)
def test_agent_plugin_service__install_agent_plugin_archive_multi(
    plugin_data_dir: Path,
    plugin_path_actual: str,
    agent_plugin_repository: IAgentPluginRepository,
    agent_plugin_service: IAgentPluginService,
    build_agent_plugin_tar_with_source_tar: Callable[[Path], BinaryIO],
):
    agent_plugin_tar = build_agent_plugin_tar_with_source_tar(plugin_data_dir / plugin_path_actual)
    agent_plugin_service.install_agent_plugin_archive(agent_plugin_tar.getvalue())

    assert agent_plugin_repository.remove_agent_plugin.call_count == 1
    assert agent_plugin_repository.store_agent_plugin.call_count == 2


def test_agent_plugin_service__plugin_install_error(
    simple_agent_plugin,
    plugin_data_dir: Path,
    agent_plugin_service: IAgentPluginService,
    build_agent_plugin_tar_with_source_tar: Callable[[Path], BinaryIO],
):
    agent_plugin_tar = build_agent_plugin_tar(
        simple_agent_plugin, manifest_file_name="manifest.idk"
    )
    with pytest.raises(PluginInstallationError):
        agent_plugin_service.install_agent_plugin_archive(agent_plugin_tar.getvalue())


@pytest.fixture
def dynamic_callback(agent_plugin_repository_index, agent_plugin_repository_index_simple):
    dynamic_responses = [agent_plugin_repository_index, agent_plugin_repository_index_simple]

    def inner(request, context) -> requests.Response:
        nonlocal dynamic_responses
        return dynamic_responses.pop(0)

    return inner


def test_agent_plugin_service__get_available_plugins(
    request_mock_instance,
    agent_plugin_service: IAgentPluginService,
    agent_plugin_repository_index,
    agent_plugin_repository_index_simple,
    dynamic_callback: Callable,
):
    request_mock_instance.get(
        AGENT_PLUGIN_REPOSITORY_URL,
        text=dynamic_callback,
    )
    actual_index_1 = agent_plugin_service.get_available_plugins(force_refresh=False)
    actual_index_2 = agent_plugin_service.get_available_plugins(force_refresh=False)

    assert actual_index_1.dict(simplify=True) == actual_index_2.dict(simplify=True)
    assert actual_index_1.dict(simplify=True) == EXPECTED_SERIALIZED_AGENT_PLUGIN_REPOSITORY_INDEX


def test_agent_plugin_service__get_available_plugins_refresh(
    request_mock_instance,
    agent_plugin_service: IAgentPluginService,
    agent_plugin_repository_index,
    agent_plugin_repository_index_simple,
    dynamic_callback: Callable,
):
    request_mock_instance.get(AGENT_PLUGIN_REPOSITORY_URL, text=dynamic_callback)

    actual_index_1 = agent_plugin_service.get_available_plugins(force_refresh=False)
    actual_index_2 = agent_plugin_service.get_available_plugins(force_refresh=False)
    actual_index_3 = agent_plugin_service.get_available_plugins(force_refresh=True)

    assert actual_index_1.dict(simplify=True) == EXPECTED_SERIALIZED_AGENT_PLUGIN_REPOSITORY_INDEX
    assert actual_index_1.dict(simplify=True) == actual_index_2.dict(simplify=True)
    assert actual_index_3.dict(simplify=True) != actual_index_2.dict(simplify=True)


def test_agent_plugin_service__get_available_plugins_exception(
    request_mock_instance,
    agent_plugin_service: IAgentPluginService,
):
    request_mock_instance.get(AGENT_PLUGIN_REPOSITORY_URL, exc=Exception)
    with pytest.raises(RetrievalError):
        agent_plugin_service.get_available_plugins(force_refresh=True)
