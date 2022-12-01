import time
from datetime import datetime, timedelta
from uuid import UUID

import pytest
import pytz
from tests.monkey_island import InMemoryAgentRepository

from common import AgentHeartbeat
from monkey_island.cc.island_event_handlers import AgentHeartbeatMonitor
from monkey_island.cc.models import Agent

AGENT_ID_1 = UUID("2d56f972-78a8-4026-9f47-2dfd550ee207")
AGENT_1 = Agent(
    id=AGENT_ID_1,
    machine_id=1,
    start_time=100,
    stop_time=None,
)

AGENT_ID_2 = UUID("65c641f2-af47-4a42-929b-109b30f0d8d6")
AGENT_2 = Agent(
    id=AGENT_ID_2,
    machine_id=2,
    start_time=100,
    stop_time=None,
)

AGENT_ID_3 = UUID("290da3c3-f410-4f5e-a472-b04416860a2c")
AGENT_3 = Agent(
    id=AGENT_ID_3,
    machine_id=3,
    start_time=300,
    stop_time=None,
)

AGENT_ID_ALREADY_STOPPED = UUID("e5cd334a-5ca5-4f19-a2ab-a68d515fea46")
AGENT_ALREADY_STOPPED = Agent(
    id=AGENT_ID_ALREADY_STOPPED,
    machine_id=4,
    start_time=600,
    stop_time=700,
)


@pytest.fixture
def in_memory_agent_repository():
    return InMemoryAgentRepository()


@pytest.fixture
def agent_heartbeat_handler(in_memory_agent_repository):
    return AgentHeartbeatMonitor(in_memory_agent_repository)


def test_multiple_agents(agent_heartbeat_handler, in_memory_agent_repository):
    in_memory_agent_repository.upsert_agent(AGENT_1)
    in_memory_agent_repository.upsert_agent(AGENT_2)
    in_memory_agent_repository.upsert_agent(AGENT_3)

    agent_heartbeat_handler.handle_agent_heartbeat(AGENT_ID_1, AgentHeartbeat(timestamp=110))
    agent_heartbeat_handler.handle_agent_heartbeat(AGENT_ID_2, AgentHeartbeat(timestamp=200))

    agent_heartbeat_handler.set_unresponsive_agents_stop_time()

    agent_1 = in_memory_agent_repository.get_agent_by_id(AGENT_ID_1)
    agent_2 = in_memory_agent_repository.get_agent_by_id(AGENT_ID_2)
    agent_3 = in_memory_agent_repository.get_agent_by_id(AGENT_ID_3)

    assert agent_1.stop_time == datetime.fromtimestamp(110, tz=pytz.UTC)
    assert agent_2.stop_time == datetime.fromtimestamp(200, tz=pytz.UTC)
    assert agent_3.stop_time == agent_3.start_time


def test_no_heartbeat_received(agent_heartbeat_handler, in_memory_agent_repository):
    in_memory_agent_repository.upsert_agent(AGENT_1)

    agent_heartbeat_handler.set_unresponsive_agents_stop_time()

    assert in_memory_agent_repository.get_agent_by_id(AGENT_ID_1).stop_time == AGENT_1.start_time


def test_agent_shutdown_unexpectedly(agent_heartbeat_handler, in_memory_agent_repository):
    last_heartbeat = datetime.fromtimestamp(8675309, tz=pytz.UTC)
    in_memory_agent_repository.upsert_agent(AGENT_1)
    agent_heartbeat_handler.handle_agent_heartbeat(
        AGENT_ID_1, AgentHeartbeat(timestamp=last_heartbeat)
    )

    agent_heartbeat_handler.set_unresponsive_agents_stop_time()

    assert in_memory_agent_repository.get_agent_by_id(AGENT_ID_1).stop_time == last_heartbeat


def test_leave_stop_time_if_heartbeat_arrives_late(
    agent_heartbeat_handler, in_memory_agent_repository
):
    in_memory_agent_repository.upsert_agent(AGENT_ALREADY_STOPPED)
    expected_stop_time = AGENT_ALREADY_STOPPED.stop_time
    heartbeat_time = AGENT_ALREADY_STOPPED.stop_time + timedelta(seconds=1000)
    agent_heartbeat_handler.handle_agent_heartbeat(
        AGENT_ID_ALREADY_STOPPED, AgentHeartbeat(timestamp=heartbeat_time)
    )

    agent_heartbeat_handler.set_unresponsive_agents_stop_time()

    assert (
        in_memory_agent_repository.get_agent_by_id(AGENT_ID_ALREADY_STOPPED).stop_time
        == expected_stop_time
    )


def test_use_latest_heartbeat(agent_heartbeat_handler, in_memory_agent_repository):
    last_heartbeat = datetime.fromtimestamp(8675309, tz=pytz.UTC)
    in_memory_agent_repository.upsert_agent(AGENT_1)
    agent_heartbeat_handler.handle_agent_heartbeat(AGENT_ID_1, AgentHeartbeat(timestamp=1000))
    agent_heartbeat_handler.handle_agent_heartbeat(
        AGENT_ID_1, AgentHeartbeat(timestamp=last_heartbeat)
    )

    agent_heartbeat_handler.set_unresponsive_agents_stop_time()

    assert in_memory_agent_repository.get_agent_by_id(AGENT_ID_1).stop_time == last_heartbeat


def test_heartbeat_not_expired(agent_heartbeat_handler, in_memory_agent_repository):
    in_memory_agent_repository.upsert_agent(AGENT_1)
    agent_heartbeat_handler.handle_agent_heartbeat(
        AGENT_ID_1, AgentHeartbeat(timestamp=time.time())
    )

    agent_heartbeat_handler.set_unresponsive_agents_stop_time()

    assert in_memory_agent_repository.get_agent_by_id(AGENT_ID_1).stop_time is None
