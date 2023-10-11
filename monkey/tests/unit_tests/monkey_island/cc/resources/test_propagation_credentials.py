import json
from http import HTTPStatus
from typing import Sequence
from urllib.parse import urljoin

import pytest
from monkeytypes import Credentials, LMHash, NTHash, Password
from tests.common import StubDIContainer
from tests.data_for_tests.propagation_credentials import LM_HASH, NT_HASH, PASSWORD_1, PASSWORD_2
from tests.monkey_island import InMemoryCredentialsRepository

from monkey_island.cc.repositories import ICredentialsRepository
from monkey_island.cc.resources import PropagationCredentials
from monkey_island.cc.resources.propagation_credentials import (
    _configured_collection,
    _stolen_collection,
)

ALL_CREDENTIALS_URL = PropagationCredentials.urls[0]
CONFIGURED_CREDENTIALS_URL = urljoin(ALL_CREDENTIALS_URL + "/", _configured_collection)
STOLEN_CREDENTIALS_URL = urljoin(ALL_CREDENTIALS_URL + "/", _stolen_collection)
CREDENTIALS_1 = Credentials(identity=None, secret=Password(password=PASSWORD_1))
CREDENTIALS_2 = Credentials(identity=None, secret=LMHash(lm_hash=LM_HASH))
CREDENTIALS_3 = Credentials(identity=None, secret=NTHash(nt_hash=NT_HASH))
CREDENTIALS_4 = Credentials(identity=None, secret=Password(password=PASSWORD_2))


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
    credentials_repository.save_configured_credentials([CREDENTIALS_1, CREDENTIALS_2])
    credentials_repository.save_stolen_credentials([CREDENTIALS_3, CREDENTIALS_4])

    resp = flask_client.get(ALL_CREDENTIALS_URL)
    actual_propagation_credentials = [Credentials(**creds) for creds in resp.json]

    assert resp.status_code == HTTPStatus.OK
    assert len(actual_propagation_credentials) == 4
    assert CREDENTIALS_1 in actual_propagation_credentials
    assert CREDENTIALS_2 in actual_propagation_credentials
    assert CREDENTIALS_3 in actual_propagation_credentials
    assert CREDENTIALS_4 in actual_propagation_credentials


def pre_populate_repository(
    url: str, credentials_repository: ICredentialsRepository, credentials: Sequence[Credentials]
):
    if "configured" in url:
        credentials_repository.save_configured_credentials(credentials)
    else:
        credentials_repository.save_stolen_credentials(credentials)


@pytest.mark.parametrize("url", [CONFIGURED_CREDENTIALS_URL, STOLEN_CREDENTIALS_URL])
def test_propagation_credentials_endpoint__get_stolen(flask_client, credentials_repository, url):
    pre_populate_repository(url, credentials_repository, [CREDENTIALS_1, CREDENTIALS_2])

    resp = flask_client.get(url)
    actual_propagation_credentials = [Credentials(**creds) for creds in resp.json]

    assert resp.status_code == HTTPStatus.OK
    assert len(actual_propagation_credentials) == 2
    assert actual_propagation_credentials[0].secret.password == PASSWORD_1
    assert actual_propagation_credentials[1].secret.lm_hash == LM_HASH


def test_configured_propagation_credentials_endpoint_put(flask_client, credentials_repository):
    pre_populate_repository(
        CONFIGURED_CREDENTIALS_URL,
        credentials_repository,
        [CREDENTIALS_1, CREDENTIALS_2],
    )
    resp = flask_client.put(CONFIGURED_CREDENTIALS_URL, json=[])
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = flask_client.get(CONFIGURED_CREDENTIALS_URL)
    assert len(json.loads(resp.text)) == 0


def test_stolen_propagation_credentials_endpoint__put_not_allowed(flask_client):
    resp = flask_client.put(STOLEN_CREDENTIALS_URL, json=[])
    assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_all_propagation_credentials_endpoint__put_not_allowed(flask_client):
    resp = flask_client.put(ALL_CREDENTIALS_URL, json=[])
    assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED


NON_EXISTENT_COLLECTION_URL = urljoin(ALL_CREDENTIALS_URL + "/", "bogus-credentials")


def test_propagation_credentials_endpoint__get_not_found(flask_client):
    resp = flask_client.get(NON_EXISTENT_COLLECTION_URL)
    assert resp.status_code == HTTPStatus.NOT_FOUND


def test_propagation_credentials_endpoint__put_not_found(flask_client):
    resp = flask_client.put(NON_EXISTENT_COLLECTION_URL, json=[])
    assert resp.status_code == HTTPStatus.NOT_FOUND
