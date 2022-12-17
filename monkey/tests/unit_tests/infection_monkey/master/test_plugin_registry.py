from unittest.mock import MagicMock

import pytest
from flask import Response

from common.agent_plugins import AgentPluginType
from infection_monkey.i_puppet import UnknownPluginError
from infection_monkey.master.plugin_registry import PluginRegistry


class StubIslandAPIClient:
    def __init__(self, status: int):
        self._status = status

    def get_plugin(self, _, __):
        return Response(status=self._status)


@pytest.fixture
def plugin_loader():
    return MagicMock()


def test_get_plugin_not_found(plugin_loader):
    plugin_registry = PluginRegistry(StubIslandAPIClient(status=404), plugin_loader)

    with pytest.raises(UnknownPluginError):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)


# modify when plugin architecture is fully implemented
def test_get_plugin_not_implemented(plugin_loader):
    plugin_registry = PluginRegistry(StubIslandAPIClient(status=200), plugin_loader)

    with pytest.raises(NotImplementedError):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)


def test_get_plugin_unexpected_response(plugin_loader):
    plugin_registry = PluginRegistry(StubIslandAPIClient(status=100), plugin_loader)

    with pytest.raises(Exception):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)
