from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import mongomock
import pytest

from monkey_island.cc.models import Agent
from monkey_island.cc.repository import (
    IAgentRepository,
    MongoAgentRepository,
    RetrievalError,
    UnknownRecordError,
)

VICTIM_ZERO_ID = uuid4()
RUNNING_AGENTS = (
    Agent(id=VICTIM_ZERO_ID, machine_id=1, start_time=datetime.fromtimestamp(1661856718)),
    Agent(
        id=uuid4(),
        machine_id=2,
        start_time=datetime.fromtimestamp(1661856818),
        parent_id=VICTIM_ZERO_ID,
    ),
)
STOPPED_AGENTS = (
    Agent(
        id=uuid4(),
        machine_id=3,
        start_time=datetime.fromtimestamp(1661856758),
        parent_id=VICTIM_ZERO_ID,
        stop_time=datetime.fromtimestamp(1661856773),
    ),
)
AGENTS = (
    *RUNNING_AGENTS,
    *STOPPED_AGENTS,
)


@pytest.fixture
def agent_repository() -> IAgentRepository:
    mongo_client = mongomock.MongoClient()
    mongo_client.monkey_island.agents.insert_many((a.dict(simplify=True) for a in AGENTS))
    return MongoAgentRepository(mongo_client)


@pytest.fixture
def error_raising_mock_mongo_client() -> mongomock.MongoClient:
    mongo_client = MagicMock(spec=mongomock.MongoClient)
    mongo_client.monkey_island = MagicMock(spec=mongomock.Database)
    mongo_client.monkey_island.agents = MagicMock(spec=mongomock.Collection)

    # The first call to find() must succeed
    mongo_client.monkey_island.agents.find_one = MagicMock(side_effect=Exception("some exception"))
    mongo_client.monkey_island.agents.find = MagicMock(side_effect=Exception("some exception"))

    return mongo_client


@pytest.fixture
def error_raising_agent_repository(error_raising_mock_mongo_client) -> IAgentRepository:
    return MongoAgentRepository(error_raising_mock_mongo_client)


def test_get_agent_by_id(agent_repository):
    for i, expected_agent in enumerate(AGENTS):
        assert agent_repository.get_agent_by_id(expected_agent.id) == expected_agent


def test_get_agent_by_id__not_found(agent_repository):
    with pytest.raises(UnknownRecordError):
        agent_repository.get_agent_by_id(uuid4())


def test_get_agent_by_id__retrieval_error(error_raising_agent_repository):
    with pytest.raises(RetrievalError):
        error_raising_agent_repository.get_agent_by_id(AGENTS[0].id)


def test_get_running_agents(agent_repository):
    running_agents = agent_repository.get_running_agents()

    assert len(running_agents) == len(RUNNING_AGENTS)
    for a in running_agents:
        assert a in RUNNING_AGENTS


def test_get_running_agents__retrieval_error(error_raising_agent_repository):
    with pytest.raises(RetrievalError):
        error_raising_agent_repository.get_running_agents()
