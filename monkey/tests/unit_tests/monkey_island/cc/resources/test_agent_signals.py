from http import HTTPStatus
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tests.common import StubDIContainer

from monkey_island.cc.event_queue import IIslandEventQueue
from monkey_island.cc.models import AgentSignals as Signals
from monkey_island.cc.repository import RetrievalError, StorageError
from monkey_island.cc.resources import AgentSignals
from monkey_island.cc.services import AgentSignalsService

TIMESTAMP = 123456789
TIMESTAMP_1 = 123546789

SIGNALS = Signals(terminate=TIMESTAMP)
SIGNALS_1 = Signals(terminate=TIMESTAMP_1)

AGENT_ID = UUID("c0dd10b3-e21a-4da9-9d96-a99c19ebd7c5")
AGENT_ID_1 = UUID("9b4279f6-6ec5-4953-821e-893ddc71a988")


@pytest.fixture
def mock_agent_signals_service():
    return MagicMock(spec=AgentSignalsService)


@pytest.fixture
def flask_client_builder(build_flask_client, mock_agent_signals_service):
    def inner(side_effect=None):
        container = StubDIContainer()

        mock_island_event_queue = MagicMock(spec=IIslandEventQueue)
        mock_island_event_queue.publish.side_effect = side_effect
        container.register_instance(IIslandEventQueue, mock_island_event_queue)

        container.register_instance(AgentSignalsService, mock_agent_signals_service)

        with build_flask_client(container) as flask_client:
            return flask_client

    return inner


@pytest.fixture
def flask_client(flask_client_builder):
    return flask_client_builder()


def test_agent_signals_terminate_all_post(flask_client):
    resp = flask_client.post(
        AgentSignals.urls[0],
        json={"kill_time": TIMESTAMP},
        follow_redirects=True,
    )
    assert resp.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.parametrize(
    "bad_data",
    [
        "bad timestamp",
        {},
        {"wrong_key": TIMESTAMP},
        TIMESTAMP,
    ],
)
def test_agent_signals_terminate_all_post__invalid_timestamp(flask_client, bad_data):
    resp = flask_client.post(
        AgentSignals.urls[0],
        json=bad_data,
        follow_redirects=True,
    )
    assert resp.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    "url, signals",
    [(f"/api/agent-signals/{AGENT_ID}", SIGNALS), (f"/api/agent-signals/{AGENT_ID_1}", SIGNALS_1)],
)
def test_agent_signals_get(flask_client, mock_agent_signals_service, url, signals):
    mock_agent_signals_service.get_signals.return_value = signals
    resp = flask_client.get(url, follow_redirects=True)
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == signals.dict(simplify=True)


@pytest.mark.parametrize(
    "url, error",
    [
        (f"/api/agent-signals/{AGENT_ID}", RetrievalError),
        (f"/api/agent-signals/{AGENT_ID_1}", StorageError),
    ],
)
def test_agent_signals_get__internal_server_error(
    flask_client, mock_agent_signals_service, url, error
):
    mock_agent_signals_service.get_signals.side_effect = error
    resp = flask_client.get(url, follow_redirects=True)
    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
