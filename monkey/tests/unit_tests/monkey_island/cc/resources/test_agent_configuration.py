import json
from http import HTTPStatus
from typing import Type
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer
from tests.common.example_agent_configuration import AGENT_CONFIGURATION
from tests.monkey_island import InMemoryAgentConfigurationService, InMemoryAgentPluginRepository
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from common.agent_configuration import AgentConfiguration
from monkey_island.cc.resources import AgentConfiguration as AgentConfigurationResource
from monkey_island.cc.services import IAgentConfigurationService, PluginConfigurationValidationError

AGENT_CONFIGURATION_URL = get_url_for_resource(AgentConfigurationResource)


@pytest.fixture
def in_memory_agent_plugin_repository():
    return InMemoryAgentPluginRepository()


@pytest.fixture
def flask_client(build_flask_client, in_memory_agent_plugin_repository):
    container = StubDIContainer()

    agent_configuration_service = InMemoryAgentConfigurationService()

    container.register_instance(IAgentConfigurationService, agent_configuration_service)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_agent_configuration_endpoint(flask_client):
    resp = flask_client.put(
        AGENT_CONFIGURATION_URL,
        json=AgentConfiguration(**AGENT_CONFIGURATION).dict(simplify=True),
        follow_redirects=True,
    )
    print(resp.data)
    assert resp.status_code == HTTPStatus.NO_CONTENT
    resp = flask_client.get(AGENT_CONFIGURATION_URL)

    assert resp.status_code == HTTPStatus.OK

    assert AgentConfiguration(**json.loads(resp.data)) == AgentConfiguration(**AGENT_CONFIGURATION)


@pytest.mark.parametrize(
    "error, expected_status",
    [
        (Exception, HTTPStatus.INTERNAL_SERVER_ERROR),
        (json.JSONDecodeError, HTTPStatus.BAD_REQUEST),
        (PluginConfigurationValidationError, HTTPStatus.BAD_REQUEST),
        (TypeError, HTTPStatus.BAD_REQUEST),
        (ValueError, HTTPStatus.BAD_REQUEST),
    ],
)
def test_agent_configuration_service_raises_exception(
    build_flask_client, error: Type[Exception], expected_status: HTTPStatus
):
    container = StubDIContainer()
    mock_agent_configuration_service = MagicMock(spec=IAgentConfigurationService)
    mock_agent_configuration_service.update_configuration = MagicMock(side_effect=error)

    container.register_instance(IAgentConfigurationService, mock_agent_configuration_service)

    with build_flask_client(container) as flask_client:
        resp = flask_client.put(
            AGENT_CONFIGURATION_URL,
            json=AgentConfiguration(**AGENT_CONFIGURATION).dict(simplify=True),
            follow_redirects=True,
        )
    assert resp.status_code == expected_status
