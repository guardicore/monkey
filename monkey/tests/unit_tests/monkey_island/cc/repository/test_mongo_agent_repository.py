from copy import deepcopy
from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import mongomock
import pytest

from monkey_island.cc.models import Agent
from monkey_island.cc.repository import (
    IAgentRepository,
    MongoAgentRepository,
    RemovalError,
    RetrievalError,
    StorageError,
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
def empty_agent_repository() -> IAgentRepository:
    mongo_client = mongomock.MongoClient()
    return MongoAgentRepository(mongo_client)


@pytest.fixture
def error_raising_mock_mongo_client() -> mongomock.MongoClient:
    mongo_client = MagicMock(spec=mongomock.MongoClient)
    mongo_client.monkey_island = MagicMock(spec=mongomock.Database)
    mongo_client.monkey_island.agents = MagicMock(spec=mongomock.Collection)

    mongo_client.monkey_island.agents.drop = MagicMock(side_effect=Exception("some exception"))
    mongo_client.monkey_island.agents.find = MagicMock(side_effect=Exception("some exception"))
    mongo_client.monkey_island.agents.find_one = MagicMock(side_effect=Exception("some exception"))
    mongo_client.monkey_island.agents.replace_one = MagicMock(
        side_effect=Exception("some exception")
    )

    return mongo_client


@pytest.fixture
def error_raising_agent_repository(error_raising_mock_mongo_client) -> IAgentRepository:
    return MongoAgentRepository(error_raising_mock_mongo_client)


def test_upsert_agent__insert(agent_repository):
    new_id = uuid4()
    new_agent = Agent(
        id=new_id,
        machine_id=2,
        start_time=datetime.fromtimestamp(1661858139),
        parent_id=VICTIM_ZERO_ID,
    )

    agent_repository.upsert_agent(new_agent)

    assert agent_repository.get_agent_by_id(new_id) == new_agent

    for agent in AGENTS:
        assert agent_repository.get_agent_by_id(agent.id) == agent


def test_upsert_agent__insert_empty_repository(empty_agent_repository):
    empty_agent_repository.upsert_agent(AGENTS[0])

    assert empty_agent_repository.get_agent_by_id(VICTIM_ZERO_ID) == AGENTS[0]


def test_upsert_agent__update(agent_repository):
    agents = deepcopy(AGENTS)
    agents[0].stop_time = datetime.now()
    agents[0].cc_server = "127.0.0.1:1984"

    agent_repository.upsert_agent(agents[0])

    for agent in agents:
        assert agent_repository.get_agent_by_id(agent.id) == agent


def test_upsert_agent__storage_error(error_raising_agent_repository):
    with pytest.raises(StorageError):
        error_raising_agent_repository.upsert_agent(AGENTS[0])


def test_upsert_agent__storage_error_update_failed(error_raising_mock_mongo_client):
    mock_result = MagicMock()
    mock_result.matched_count = 1
    mock_result.modified_count = 0

    error_raising_mock_mongo_client.monkey_island.agents.replace_one = MagicMock(
        return_value=mock_result
    )
    agent_repository = MongoAgentRepository(error_raising_mock_mongo_client)

    agent = AGENTS[0]
    with pytest.raises(StorageError):
        agent_repository.upsert_agent(agent)


def test_upsert_agent__storage_error_insert_failed(error_raising_mock_mongo_client):
    mock_result = MagicMock()
    mock_result.matched_count = 0
    mock_result.upserted_id = None

    error_raising_mock_mongo_client.monkey_island.agents.replace_one = MagicMock(
        return_value=mock_result
    )
    agent_repository = MongoAgentRepository(error_raising_mock_mongo_client)

    agent = AGENTS[0]
    with pytest.raises(StorageError):
        agent_repository.upsert_agent(agent)


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


def test_reset(agent_repository):
    # Ensure the repository is not empty
    for agent in AGENTS:
        preexisting_agent = agent_repository.get_agent_by_id(agent.id)
        assert isinstance(preexisting_agent, Agent)

    agent_repository.reset()

    for agent in AGENTS:
        with pytest.raises(UnknownRecordError):
            agent_repository.get_agent_by_id(agent.id)


def test_usable_after_reset(agent_repository):
    agent_repository.reset()

    agent_repository.upsert_agent(AGENTS[0])

    assert agent_repository.get_agent_by_id(VICTIM_ZERO_ID) == AGENTS[0]


def test_reset__removal_error(error_raising_agent_repository):
    with pytest.raises(RemovalError):
        error_raising_agent_repository.reset()
