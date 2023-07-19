import pytest
from tests.monkey_island import InMemoryAgentConfigurationRepository, InMemoryAgentPluginRepository

from common.base_models import MutableInfectionMonkeyBaseModel
from monkey_island.cc.repositories import RetrievalError
from monkey_island.cc.services import PluginConfigurationValidationError
from monkey_island.cc.services.agent_configuration_service.agent_configuration_schema_compiler import (  # noqa: E501
    AgentConfigurationSchemaCompiler,
)
from monkey_island.cc.services.agent_configuration_service.agent_configuration_validation_decorator import (  # noqa: E501
    AgentConfigurationValidationDecorator,
)
from monkey_island.cc.services.agent_configuration_service.i_agent_configuration_repository import (  # noqa: E501
    IAgentConfigurationRepository,
)


class FakeConfiguration(MutableInfectionMonkeyBaseModel):
    some_field: str
    other_field: float


@pytest.fixture
def fake_configuration():
    return FakeConfiguration(some_field="bla", other_field=1.1)


@pytest.fixture
def in_memory_agent_configuration_repository() -> IAgentConfigurationRepository:
    return InMemoryAgentConfigurationRepository()


@pytest.fixture
def in_memory_agent_plugin_repository() -> InMemoryAgentPluginRepository:
    return InMemoryAgentPluginRepository()


@pytest.fixture
def agent_configuration_repository(
    in_memory_agent_plugin_repository, in_memory_agent_configuration_repository
):
    agent_configuration_schema_compiler = AgentConfigurationSchemaCompiler(
        in_memory_agent_plugin_repository
    )
    agent_configuration_repository_decorated = AgentConfigurationValidationDecorator(
        in_memory_agent_configuration_repository, agent_configuration_schema_compiler
    )
    return agent_configuration_repository_decorated


def test_get_configuration_validated(
    in_memory_agent_configuration_repository, agent_configuration_repository
):
    expected_configuration = in_memory_agent_configuration_repository.get_configuration()

    actual_configuration = agent_configuration_repository.get_configuration()

    assert actual_configuration == expected_configuration


def test_get_configuration_raise_retrieval_error(
    fake_configuration, in_memory_agent_configuration_repository, agent_configuration_repository
):
    in_memory_agent_configuration_repository.update_configuration(fake_configuration)

    with pytest.raises(RetrievalError):
        agent_configuration_repository.get_configuration()


def test_update_configuration_validated(
    default_agent_configuration,
    in_memory_agent_configuration_repository,
    in_memory_agent_plugin_repository,
    agent_configuration_repository,
):
    agent_configuration_repository.update_configuration(default_agent_configuration)

    expected_configuration = in_memory_agent_configuration_repository.get_configuration()

    assert default_agent_configuration == expected_configuration


def test_update_configuration_raise_plugin_configuration_validation_error(
    fake_configuration, in_memory_agent_configuration_repository, agent_configuration_repository
):
    in_memory_agent_configuration_repository.update_configuration(fake_configuration)

    with pytest.raises(PluginConfigurationValidationError):
        agent_configuration_repository.update_configuration(fake_configuration)
