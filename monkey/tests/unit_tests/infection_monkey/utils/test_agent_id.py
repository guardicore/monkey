from uuid import UUID

from infection_monkey.utils.agent_id import get_agent_id


def test_get_agent_id():
    agent_id = get_agent_id()

    assert isinstance(agent_id, UUID)
    assert agent_id == get_agent_id()
