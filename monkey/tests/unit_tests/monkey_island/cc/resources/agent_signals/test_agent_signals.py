from http import HTTPStatus
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tests.common import StubDIContainer

from common.agent_signals import AgentSignals as Signals
from monkey_island.cc.repositories import RetrievalError, StorageError
from monkey_island.cc.services import AgentSignalsService

TIMESTAMP_1 = 123456789
TIMESTAMP_2 = 123546789

SIGNALS_1 = Signals(terminate=TIMESTAMP_1)
SIGNALS_2 = Signals(terminate=TIMESTAMP_2)

AGENT_ID_1 = UUID("c0dd10b3-e21a-4da9-9d96-a99c19ebd7c5")
AGENT_ID_2 = UUID("9b4279f6-6ec5-4953-821e-893ddc71a988")


@pytest.fixture
def mock_agent_signals_service():
    return MagicMock(spec=AgentSignalsService)


@pytest.fixture
def flask_client(build_flask_client, mock_agent_signals_service):
    container = StubDIContainer()
    container.register_instance(AgentSignalsService, mock_agent_signals_service)

    with build_flask_client(container) as flask_client:
        yield flask_client


@pytest.mark.parametrize(
    "url, signals",
    [
        (f"/api/agent-signals/{AGENT_ID_1}", SIGNALS_1),
        (f"/api/agent-signals/{AGENT_ID_2}", SIGNALS_2),
    ],
)
def test_agent_signals_get(flask_client, mock_agent_signals_service, url, signals):
    mock_agent_signals_service.get_signals.return_value = signals
    resp = flask_client.get(url, follow_redirects=True)
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == signals.to_json_dict()


@pytest.mark.parametrize(
    "url, error",
    [
        (f"/api/agent-signals/{AGENT_ID_1}", RetrievalError),
        (f"/api/agent-signals/{AGENT_ID_2}", StorageError),
    ],
)
def test_agent_signals_get__internal_server_error(
    flask_client, mock_agent_signals_service, url, error
):
    mock_agent_signals_service.get_signals.side_effect = error
    resp = flask_client.get(url, follow_redirects=True)
    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
