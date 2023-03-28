from uuid import UUID

from infection_monkey.utils.ids import get_agent_id, get_machine_id


def test_get_agent_id():
    agent_id = get_agent_id()

    assert isinstance(agent_id, UUID)


def test_get_agent_id__is_unique():
    agent_id = get_agent_id()

    assert agent_id != get_agent_id()


def test_get_machine_id():
    machine_id = get_machine_id()

    assert isinstance(machine_id, int)
    assert machine_id == get_machine_id()
