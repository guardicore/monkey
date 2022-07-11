import json

from tests.data_for_tests.propagation_credentials import (
    PROPAGATION_CREDENTIALS_1,
    PROPAGATION_CREDENTIALS_2,
)
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.resources.credentials.stolen_propagation_credentials import (
    StolenPropagationCredentials,
)


def test_stolen_propagation_credentials_endpoint_get(flask_client):
    stolen_propagation_credentials_url = get_url_for_resource(StolenPropagationCredentials)

    resp = flask_client.get(stolen_propagation_credentials_url)

    assert resp.status_code == 200
    actual_propagation_credentials = json.loads(resp.data)
    assert len(actual_propagation_credentials) == 2

    # TODO: delete the removal of monkey_guid key when the serialization of credentials
    del actual_propagation_credentials[0]["monkey_guid"]
    assert actual_propagation_credentials[0] == PROPAGATION_CREDENTIALS_1
    del actual_propagation_credentials[1]["monkey_guid"]
    assert actual_propagation_credentials[1] == PROPAGATION_CREDENTIALS_2


def test_stolen_propagation_credentials_endpoint_post(flask_client):
    stolen_propagation_credentials_url = get_url_for_resource(StolenPropagationCredentials)

    resp = flask_client.post(stolen_propagation_credentials_url, json=PROPAGATION_CREDENTIALS_1)

    assert resp.status_code == 204


def test_stolen_propagation_credentials_endpoint_delete(flask_client):
    stolen_propagation_credentials_url = get_url_for_resource(StolenPropagationCredentials)

    resp = flask_client.delete(stolen_propagation_credentials_url)

    assert resp.status_code == 204
