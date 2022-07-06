import json

import pytest
from tests.common import StubDIContainer
from tests.monkey_island import StubPropagationCredentialsRepository
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.repository import ICredentialsRepository
from monkey_island.cc.resources.propagation_credentials import PropagationCredentials


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()

    container.register(ICredentialsRepository, StubPropagationCredentialsRepository)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_propagation_credentials_endpoint_get(flask_client):
    propagation_credentials_url = get_url_for_resource(PropagationCredentials)

    resp = flask_client.get(propagation_credentials_url)

    assert resp.status_code == 200
    assert len(json.loads(resp.data)["propagation_credentials"]) == 2
