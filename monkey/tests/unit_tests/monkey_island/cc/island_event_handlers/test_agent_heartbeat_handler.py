import copy
from datetime import datetime
from uuid import UUID

import pytest
import pytz
from tests.monkey_island import InMemoryAgentRepository

from common import AgentHeartbeat
from common.types import SocketAddress
from monkey_island.cc.island_event_handlers import AgentHeartbeatHandler
from monkey_island.cc.models import Agent

AGENT_ID_1 = UUID("2d56f972-78a8-4026-9f47-2dfd550ee207")
AGENT_ID_2 = UUID("65c641f2-af47-4a42-929b-109b30f0d8d6")
AGENT_ID_4 = UUID("e5cd334a-5ca5-4f19-a2ab-a68d515fea46")

AGENTS = [
    Agent(
        id=AGENT_ID_1,
        machine_id=1,
        start_time=100,
        stop_time=None,
        cc_server=SocketAddress(ip="127.0.0.1", port=5000),
    ),
    Agent(
        id=AGENT_ID_2,
        machine_id=2,
        start_time=100,
        stop_time=None,
        cc_server=SocketAddress(ip="127.0.0.1", port=5000),
    ),
    Agent(
        id=UUID("290da3c3-f410-4f5e-a472-b04416860a2c"),
        machine_id=3,
        start_time=300,
        stop_time=700,
        cc_server=SocketAddress(ip="127.0.0.1", port=5000),
    ),
    Agent(
        id=AGENT_ID_4,
        machine_id=4,
        start_time=600,
        stop_time=None,
        cc_server=SocketAddress(ip="127.0.0.1", port=5000),
    ),
]


@pytest.fixture
def in_memory_agent_repository():
    in_memory_agent_repository = InMemoryAgentRepository()
    for agent in copy.deepcopy(AGENTS):
        in_memory_agent_repository.upsert_agent(agent)

    return in_memory_agent_repository


@pytest.fixture
def agent_heartbeat_handler(in_memory_agent_repository):
    return AgentHeartbeatHandler(in_memory_agent_repository)


def test_agent_heartbeat_handler__no_heartbeats(
    agent_heartbeat_handler, in_memory_agent_repository
):
    agent_heartbeat_handler.update_agents_stop_time_from_heartbeat()

    actual_running_agents = in_memory_agent_repository.get_running_agents()
    assert len(actual_running_agents) == 0

    actual_agents = in_memory_agent_repository.get_agents()
    assert actual_agents[0].stop_time == actual_agents[0].start_time


def test_agent_heartbeat_handler__heartbeats(agent_heartbeat_handler, in_memory_agent_repository):
    agent_heartbeat_handler.update_agent_last_heartbeat(AGENT_ID_1, AgentHeartbeat(timestamp=110))
    agent_heartbeat_handler.update_agent_last_heartbeat(AGENT_ID_2, AgentHeartbeat(timestamp=200))

    agent_heartbeat_handler.update_agents_stop_time_from_heartbeat()

    actual_agent_1 = in_memory_agent_repository.get_agent_by_id(AGENT_ID_1)
    actual_agent_2 = in_memory_agent_repository.get_agent_by_id(AGENT_ID_2)

    assert actual_agent_1.stop_time == datetime.fromtimestamp(110, tz=pytz.UTC)
    assert actual_agent_2.stop_time == datetime.fromtimestamp(200, tz=pytz.UTC)
