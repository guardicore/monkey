import json
from http import HTTPStatus

import pytest
from tests.common import StubDIContainer
from tests.data_for_tests.propagation_credentials import (
    PROPAGATION_CREDENTIALS_1,
    PROPAGATION_CREDENTIALS_2,
    PROPAGATION_CREDENTIALS_3,
    PROPAGATION_CREDENTIALS_4,
)
from tests.monkey_island import InMemoryCredentialsRepository

from common.credentials import Credentials
from monkey_island.cc.repository import ICredentialsRepository
from monkey_island.cc.resources.credentials.propagation_credentials import PropagationCredentials

ALL_CREDENTIALS_URL = PropagationCredentials.urls[0]
STOLEN_CREDENTIALS_URL = PropagationCredentials.urls[1]


@pytest.fixture
def credentials_repository():
    return InMemoryCredentialsRepository()


@pytest.fixture
def flask_client(build_flask_client, credentials_repository):
    container = StubDIContainer()

    container.register_instance(ICredentialsRepository, credentials_repository)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_propagation_credentials_endpoint_get(flask_client, credentials_repository):
    credentials_repository.save_configured_credentials(
        [PROPAGATION_CREDENTIALS_1, PROPAGATION_CREDENTIALS_3]
    )
    credentials_repository.save_stolen_credentials(
        [PROPAGATION_CREDENTIALS_2, PROPAGATION_CREDENTIALS_4]
    )

    resp = flask_client.get(ALL_CREDENTIALS_URL)
    actual_propagation_credentials = Credentials.from_json_array(resp.text)

    assert resp.status_code == HTTPStatus.OK
    assert len(actual_propagation_credentials) == 4
    assert PROPAGATION_CREDENTIALS_1 in actual_propagation_credentials
    assert PROPAGATION_CREDENTIALS_2 in actual_propagation_credentials
    assert PROPAGATION_CREDENTIALS_3 in actual_propagation_credentials
    assert PROPAGATION_CREDENTIALS_4 in actual_propagation_credentials


def test_propagation_credentials_endpoint__get_stolen(flask_client, credentials_repository):
    credentials_repository.save_stolen_credentials(
        [PROPAGATION_CREDENTIALS_1, PROPAGATION_CREDENTIALS_2]
    )

    resp = flask_client.get(STOLEN_CREDENTIALS_URL)
    actual_propagation_credentials = Credentials.from_json_array(resp.text)

    assert resp.status_code == HTTPStatus.OK
    assert len(actual_propagation_credentials) == 2
    assert actual_propagation_credentials[0] == PROPAGATION_CREDENTIALS_1
    assert actual_propagation_credentials[1] == PROPAGATION_CREDENTIALS_2


def test_propagation_credentials_endpoint__post_stolen(flask_client, credentials_repository):
    credentials_repository.save_stolen_credentials([PROPAGATION_CREDENTIALS_1])

    resp = flask_client.post(
        STOLEN_CREDENTIALS_URL,
        json=[
            Credentials.to_json(PROPAGATION_CREDENTIALS_2),
            Credentials.to_json(PROPAGATION_CREDENTIALS_3),
        ],
    )
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = flask_client.get(STOLEN_CREDENTIALS_URL)
    retrieved_propagation_credentials = Credentials.from_json_array(resp.text)

    assert resp.status_code == HTTPStatus.OK
    assert len(retrieved_propagation_credentials) == 3
    assert PROPAGATION_CREDENTIALS_1 in retrieved_propagation_credentials
    assert PROPAGATION_CREDENTIALS_2 in retrieved_propagation_credentials
    assert PROPAGATION_CREDENTIALS_3 in retrieved_propagation_credentials


def test_stolen_propagation_credentials_endpoint_delete(flask_client, credentials_repository):
    credentials_repository.save_stolen_credentials(
        [PROPAGATION_CREDENTIALS_1, PROPAGATION_CREDENTIALS_2]
    )
    resp = flask_client.delete(STOLEN_CREDENTIALS_URL)
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = flask_client.get(STOLEN_CREDENTIALS_URL)
    assert len(json.loads(resp.text)) == 0


def test_propagation_credentials_endpoint__propagation_credentials_post_not_allowed(flask_client):
    resp = flask_client.post(ALL_CREDENTIALS_URL, json=[])
    assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_propagation_credentials_endpoint__propagation_credentials_delete_not_allowed(flask_client):
    resp = flask_client.delete(ALL_CREDENTIALS_URL)
    assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED
