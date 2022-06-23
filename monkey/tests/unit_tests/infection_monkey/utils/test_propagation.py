import pytest

from common.configuration import AgentConfiguration, AgentConfigurationSchema
from infection_monkey.utils.propagation import should_propagate


@pytest.fixture
def get_config(default_agent_configuration):
    def _inner(max_depth):
        # AgentConfiguration is a frozen dataclass, so we need to deserialize and reserialize to
        # modify it. The benefit is that it's impossible to construct an invalid object. The
        # downside is the extra steps required to change an object. Maybe we can come up with a
        # better all-around solution. It depends how often we need to mutate these objects (probably
        # only for tests).
        agent_dict = AgentConfigurationSchema().dump(default_agent_configuration)
        agent_dict["propagation"]["maximum_depth"] = max_depth

        return AgentConfiguration.from_dict(agent_dict)

    return _inner


def test_should_propagate_current_less_than_max(get_config):
    max_depth = 2
    current_depth = 1

    config = get_config(max_depth)

    assert should_propagate(config, current_depth) is True


def test_should_propagate_current_greater_than_max(get_config):
    max_depth = 2
    current_depth = 3

    config = get_config(max_depth)

    assert should_propagate(config, current_depth) is False


def test_should_propagate_current_equal_to_max(get_config):
    max_depth = 2
    current_depth = max_depth

    config = get_config(max_depth)

    assert should_propagate(config, current_depth) is False
