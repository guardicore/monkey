from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.resources import AgentConfigurationSchema
from monkey_island.cc.services import ConfigSchemaService

AGENT_CONFIGURATION_SCHEMA_URL = get_url_for_resource(AgentConfigurationSchema)


@pytest.fixture
def mock_config_schema_service():
    return MagicMock(spec=ConfigSchemaService)


@pytest.fixture
def flask_client(build_flask_client, mock_config_schema_service):
    container = StubDIContainer()
    container.register_instance(ConfigSchemaService, mock_config_schema_service)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_agent_configuration_schema_endpoint(flask_client, mock_config_schema_service):
    mock_config_schema_service.get_schema = lambda: {}

    resp = flask_client.get(AGENT_CONFIGURATION_SCHEMA_URL)

    assert resp.status_code == 200


def test_agent_configuration_schema_endpoint_error(flask_client, mock_config_schema_service):
    def raise_runtime_error():
        raise RuntimeError

    mock_config_schema_service.get_schema = raise_runtime_error

    resp = flask_client.get(AGENT_CONFIGURATION_SCHEMA_URL)

    assert resp.status_code == 500
