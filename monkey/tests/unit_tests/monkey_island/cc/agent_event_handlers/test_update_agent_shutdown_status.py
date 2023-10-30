from datetime import datetime
from uuid import UUID

import pytest
import pytz
from monkeytypes import SocketAddress
from tests.monkey_island import InMemoryAgentRepository

from common.agent_events import AgentShutdownEvent
from monkey_island.cc.agent_event_handlers import update_agent_shutdown_status
from monkey_island.cc.models import Agent
from monkey_island.cc.repositories import IAgentRepository, UnknownRecordError

AGENT_ID = UUID("1d8ce743-a0f4-45c5-96af-91106529d3e2")
AGENT_SHA256 = "35f129207bbe966ef786d0db4aab5113f3d6ea673a0c6890c2e9116617c9816f"
MACHINE_ID = 11
CC_SERVER = SocketAddress(ip="10.10.10.100", port="5000")


def get_agent_object() -> Agent:
    return Agent(
        id=AGENT_ID,
        machine_id=MACHINE_ID,
        start_time=0,
        parent_id=None,
        cc_server=CC_SERVER,
        sha256=AGENT_SHA256,
    )


TIMESTAMP = 123.321
AGENT_SHUTDOWN_EVENT = AgentShutdownEvent(source=AGENT_ID, timestamp=TIMESTAMP)


@pytest.fixture
def agent_repository() -> IAgentRepository:
    agent_repository = InMemoryAgentRepository()
    agent_repository.upsert_agent(get_agent_object())
    return agent_repository


def test_update_agent_shutdown_status(agent_repository):
    update_agent_shutdown_status_handler = update_agent_shutdown_status(agent_repository)

    update_agent_shutdown_status_handler(AGENT_SHUTDOWN_EVENT)

    assert agent_repository.get_agent_by_id(AGENT_ID).stop_time == datetime.fromtimestamp(
        TIMESTAMP, tz=pytz.UTC
    )


def test_update_agent_shutdown_status__unknown_record_error_raised(agent_repository):
    another_agent_shutdown_event = AgentShutdownEvent(
        source=UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10"), timestamp=TIMESTAMP
    )
    update_agent_shutdown_status_handler = update_agent_shutdown_status(agent_repository)

    with pytest.raises(UnknownRecordError):
        update_agent_shutdown_status_handler(another_agent_shutdown_event)
