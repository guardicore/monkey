from http import HTTPStatus
from uuid import UUID

import pytest
from tests.common import StubDIContainer
from tests.monkey_island import InMemoryAgentLogRepository

from monkey_island.cc.repositories import IAgentLogRepository

AGENT_ID_1 = UUID("c0dd10b3-e21a-4da9-9d96-a99c19ebd7c5")
AGENT_ID_2 = UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5")

AGENT_LOGS_URL_1 = f"/api/agent-logs/{AGENT_ID_1}"
AGENT_LOGS_URL_2 = f"/api/agent-logs/{AGENT_ID_2}"


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()
    container.register_instance(IAgentLogRepository, InMemoryAgentLogRepository())

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_agent_logs_endpoint__get_empty(flask_client):
    resp = flask_client.get(AGENT_LOGS_URL_1, follow_redirects=True)
    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json == ""


@pytest.mark.parametrize(
    "url,log", [(AGENT_LOGS_URL_1, "LoremIpsum1"), (AGENT_LOGS_URL_2, "SecondLoremIpsum")]
)
def test_agent_logs_endpoint(flask_client, url, log):
    flask_client.put(url, json=log, follow_redirects=True)
    resp = flask_client.get(url, follow_redirects=True)
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == log
