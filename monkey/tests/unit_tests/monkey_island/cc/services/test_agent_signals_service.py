from unittest.mock import MagicMock
from uuid import UUID

import pytest

from common.types import AgentID
from monkey_island.cc.models import Agent, Simulation
from monkey_island.cc.repository import IAgentRepository, ISimulationRepository, UnknownRecordError
from monkey_island.cc.services import AgentSignalsService

AGENT_1 = Agent(
    id=UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5"),
    machine_id=1,
    start_time=100,
    parent_id=None,
)

AGENT_2 = Agent(
    id=UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10"),
    machine_id=2,
    start_time=200,
    parent_id=AGENT_1.id,
)

AGENT_3 = Agent(
    id=UUID("0fc9afcb-1902-436b-bd5c-1ad194252484"),
    machine_id=3,
    start_time=300,
    parent_id=AGENT_2.id,
)
AGENTS = [AGENT_1, AGENT_2, AGENT_3]


@pytest.fixture
def mock_simulation_repository() -> IAgentRepository:
    return MagicMock(spec=ISimulationRepository)


@pytest.fixture(scope="session")
def mock_agent_repository() -> IAgentRepository:
    def get_agent_by_id(agent_id: AgentID) -> Agent:
        for agent in AGENTS:
            if agent.id == agent_id:
                return agent

        raise UnknownRecordError(str(agent_id))

    agent_repository = MagicMock(spec=IAgentRepository)
    agent_repository.get_progenitor = MagicMock(return_value=AGENT_1)
    agent_repository.get_agent_by_id = MagicMock(side_effect=get_agent_by_id)

    return agent_repository


@pytest.fixture
def agent_signals_service(mock_simulation_repository, mock_agent_repository) -> AgentSignalsService:
    return AgentSignalsService(mock_simulation_repository, mock_agent_repository)


@pytest.mark.parametrize("agent", AGENTS)
def test_terminate_is_none(
    agent,
    agent_signals_service: AgentSignalsService,
    mock_simulation_repository: ISimulationRepository,
):
    mock_simulation_repository.get_simulation = MagicMock(
        return_value=Simulation(terminate_signal_time=None)
    )

    signals = agent_signals_service.get_signals(agent.id)
    assert signals.terminate is None


@pytest.mark.parametrize("agent", AGENTS)
def test_agent_started_before_terminate(
    agent,
    agent_signals_service: AgentSignalsService,
    mock_simulation_repository: ISimulationRepository,
):
    TERMINATE_TIMESTAMP = 400
    mock_simulation_repository.get_simulation = MagicMock(
        return_value=Simulation(terminate_signal_time=TERMINATE_TIMESTAMP)
    )

    signals = agent_signals_service.get_signals(agent.id)

    assert signals.terminate.timestamp() == TERMINATE_TIMESTAMP


@pytest.mark.parametrize("agent", AGENTS)
def test_agent_started_after_terminate(
    agent,
    agent_signals_service: AgentSignalsService,
    mock_simulation_repository: ISimulationRepository,
):
    TERMINATE_TIMESTAMP = 50
    mock_simulation_repository.get_simulation = MagicMock(
        return_value=Simulation(terminate_signal_time=TERMINATE_TIMESTAMP)
    )

    signals = agent_signals_service.get_signals(agent.id)

    assert signals.terminate is None


@pytest.mark.parametrize("agent", AGENTS)
def test_progenitor_started_before_terminate(
    agent,
    agent_signals_service: AgentSignalsService,
    mock_simulation_repository: ISimulationRepository,
):
    TERMINATE_TIMESTAMP = 150
    mock_simulation_repository.get_simulation = MagicMock(
        return_value=Simulation(terminate_signal_time=TERMINATE_TIMESTAMP)
    )

    signals = agent_signals_service.get_signals(agent.id)

    assert signals.terminate.timestamp() == TERMINATE_TIMESTAMP
