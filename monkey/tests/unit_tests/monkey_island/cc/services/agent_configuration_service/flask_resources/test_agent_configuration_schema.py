from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.repositories import RetrievalError
from monkey_island.cc.services import IAgentConfigurationService
from monkey_island.cc.services.agent_configuration_service.flask_resources.agent_configuration_schema import (  # noqa: E501
    AgentConfigurationSchema,
)

AGENT_CONFIGURATION_SCHEMA_URL = get_url_for_resource(AgentConfigurationSchema)


@pytest.fixture
def mock_agent_configuration_service():
    return MagicMock(spec=IAgentConfigurationService)


@pytest.fixture
def flask_client(build_flask_client, mock_agent_configuration_service):
    container = StubDIContainer()
    container.register_instance(IAgentConfigurationService, mock_agent_configuration_service)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_agent_configuration_schema_endpoint(flask_client, mock_agent_configuration_service):
    fake_schema = {"schema": True}
    mock_agent_configuration_service.get_schema = lambda: fake_schema

    resp = flask_client.get(AGENT_CONFIGURATION_SCHEMA_URL)

    assert resp.status_code == HTTPStatus.OK
    assert resp.json == fake_schema


def test_agent_configuration_schema_endpoint_error(flask_client, mock_agent_configuration_service):
    mock_agent_configuration_service.get_schema = MagicMock(side_effect=RuntimeError)

    resp = flask_client.get(AGENT_CONFIGURATION_SCHEMA_URL)

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_agent_configuration_schema_endpoint_retrieval_error(
    flask_client, mock_agent_configuration_service
):
    mock_agent_configuration_service.get_schema = MagicMock(side_effect=RetrievalError)

    resp = flask_client.get(AGENT_CONFIGURATION_SCHEMA_URL)

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
