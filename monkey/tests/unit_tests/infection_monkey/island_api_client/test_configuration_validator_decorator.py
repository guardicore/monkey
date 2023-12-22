from copy import deepcopy
from unittest.mock import MagicMock

import pytest
from tests.common.example_agent_configuration import AGENT_CONFIGURATION

from common.agent_configuration import AgentConfiguration
from infection_monkey.island_api_client import (
    ConfigurationValidatorDecorator,
    IIslandAPIClient,
    IslandAPIError,
)

from .configuration_validation_constants import SCHEMA


@pytest.fixture
def fake_island_api_client():
    fake_island_api_client = MagicMock(spec=IIslandAPIClient)
    fake_island_api_client.get_agent_configuration_schema = lambda: SCHEMA
    return fake_island_api_client


def test_get_config__valid_config(fake_island_api_client):
    fake_island_api_client.get_config = lambda: AgentConfiguration(**AGENT_CONFIGURATION)
    decorated_island_api_client = ConfigurationValidatorDecorator(fake_island_api_client)

    configuration_received = decorated_island_api_client.get_config()

    assert configuration_received == AgentConfiguration(**AGENT_CONFIGURATION)


def test_get_config__invalid_config(fake_island_api_client):
    invalid_config = deepcopy(AGENT_CONFIGURATION)
    invalid_config["keep_tunnel_open_time"] = "not a number"

    fake_island_api_client.get_config = lambda: AgentConfiguration.model_construct(**invalid_config)
    decorated_island_api_client = ConfigurationValidatorDecorator(fake_island_api_client)

    with pytest.raises(IslandAPIError):
        decorated_island_api_client.get_config()
