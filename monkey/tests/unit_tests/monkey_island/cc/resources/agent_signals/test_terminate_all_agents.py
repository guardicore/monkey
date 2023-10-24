from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer

from monkey_island.cc.event_queue import IIslandEventQueue
from monkey_island.cc.models import TerminateAllAgents as TerminateAllAgentsObject
from monkey_island.cc.resources import TerminateAllAgents

TIMESTAMP = 123456789


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()

    mock_island_event_queue = MagicMock(spec=IIslandEventQueue)
    mock_island_event_queue.publish.side_effect = None
    container.register_instance(IIslandEventQueue, mock_island_event_queue)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_terminate_all_agents_post(flask_client):
    terminate_all_agents = TerminateAllAgentsObject(timestamp=TIMESTAMP)
    resp = flask_client.post(
        TerminateAllAgents.urls[0],
        json=terminate_all_agents.to_json_dict(),
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
        {"terminate_time": 0},
        {"terminate_time": -1},
    ],
)
def test_terminate_all_agents_post__invalid_timestamp(flask_client, bad_data):
    resp = flask_client.post(
        TerminateAllAgents.urls[0],
        json=bad_data,
        follow_redirects=True,
    )
    assert resp.status_code == HTTPStatus.BAD_REQUEST
