from http import HTTPStatus
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tests.common import StubDIContainer

from monkey_island.cc.event_queue import IIslandEventQueue
from monkey_island.cc.resources import AgentSignals
from monkey_island.cc.services import AgentSignalsService

TIMESTAMP = 123456789


@pytest.fixture(
    params=[
        UUID("c0dd10b3-e21a-4da9-9d96-a99c19ebd7c5"),
        UUID("9b4279f6-6ec5-4953-821e-893ddc71a988"),
    ]
)
def agent_id(request) -> UUID:
    return request.param


@pytest.fixture
def agent_signals_url(agent_id: UUID) -> str:
    return f"/api/agent-signals/{agent_id}"


@pytest.fixture
def flask_client_builder(build_flask_client):
    def inner(side_effect=None):
        container = StubDIContainer()

        mock_island_event_queue = MagicMock(spec=IIslandEventQueue)
        mock_island_event_queue.publish.side_effect = side_effect
        container.register_instance(IIslandEventQueue, mock_island_event_queue)

        mock_agent_signals_service = MagicMock(spec=AgentSignalsService)
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


# TODO: Complete this when GET is implemented
# Do we get a value indicating that we should stop? Depends on whether a signal was sent
def test_agent_signals_endpoint(flask_client, agent_signals_url):
    resp = flask_client.get(agent_signals_url, follow_redirects=True)
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == {}
