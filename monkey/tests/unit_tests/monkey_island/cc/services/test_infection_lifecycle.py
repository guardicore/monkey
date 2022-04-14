import uuid

import pytest

from monkey_island.cc.models import Config, Monkey
from monkey_island.cc.models.agent_controls import AgentControls
from monkey_island.cc.services.infection_lifecycle import should_agent_die


@pytest.mark.usefixtures("uses_database")
def test_should_agent_die_by_config(monkeypatch):
    monkey = Monkey(guid=str(uuid.uuid4()))
    monkey.config = Config(should_stop=True)
    monkey.save()
    assert should_agent_die(monkey.guid)

    monkeypatch.setattr(
        "monkey_island.cc.services.infection_lifecycle._is_monkey_killed_manually", lambda _: False
    )
    monkey.config.should_stop = True
    monkey.save()
    assert not should_agent_die(monkey.guid)


def create_monkey(launch_time):
    monkey = Monkey(guid=str(uuid.uuid4()))
    monkey.config = Config(should_stop=False)
    monkey.launch_time = launch_time
    monkey.save()
    return monkey


@pytest.mark.usefixtures("uses_database")
def test_should_agent_die_no_kill_event():
    monkey = create_monkey(launch_time=3)
    kill_event = AgentControls()
    kill_event.save()
    assert not should_agent_die(monkey.guid)


def create_kill_event(event_time):
    kill_event = AgentControls(last_stop_all=event_time)
    kill_event.save()
    return kill_event


def create_parent(child_monkey, launch_time):
    monkey_parent = Monkey(guid=str(uuid.uuid4()))
    child_monkey.parent = [[monkey_parent.guid]]
    monkey_parent.launch_time = launch_time
    monkey_parent.save()
    child_monkey.save()


@pytest.mark.usefixtures("uses_database")
def test_was_agent_killed_manually(monkeypatch):
    monkey = create_monkey(launch_time=2)

    create_kill_event(event_time=3)

    assert should_agent_die(monkey.guid)


@pytest.mark.usefixtures("uses_database")
def test_agent_killed_on_wakeup(monkeypatch):
    monkey = create_monkey(launch_time=2)

    create_kill_event(event_time=2)

    assert should_agent_die(monkey.guid)


@pytest.mark.usefixtures("uses_database")
def test_manual_kill_dont_affect_new_monkeys(monkeypatch):
    monkey = create_monkey(launch_time=3)

    create_kill_event(event_time=2)

    assert not should_agent_die(monkey.guid)


@pytest.mark.usefixtures("uses_database")
def test_parent_manually_killed(monkeypatch):
    monkey = create_monkey(launch_time=3)
    create_parent(child_monkey=monkey, launch_time=1)

    create_kill_event(event_time=2)

    assert should_agent_die(monkey.guid)


@pytest.mark.usefixtures("uses_database")
def test_parent_manually_killed_on_wakeup(monkeypatch):
    monkey = create_monkey(launch_time=3)
    create_parent(child_monkey=monkey, launch_time=2)

    create_kill_event(event_time=2)

    assert should_agent_die(monkey.guid)


@pytest.mark.usefixtures("uses_database")
def test_manual_kill_dont_affect_new_monkeys_with_parent(monkeypatch):
    monkey = create_monkey(launch_time=3)
    create_parent(child_monkey=monkey, launch_time=2)

    create_kill_event(event_time=1)

    assert not should_agent_die(monkey.guid)
