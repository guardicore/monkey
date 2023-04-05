from uuid import UUID

import pytest
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME, REFRESH_TOKEN_KEY_NAME
from monkey_island.cc.services.authentication_service.flask_resources.agent_otp_login import (
    AgentOTPLogin,
)

AGENT_ID = UUID("9614480d-471b-4568-86b5-cb922a34ed8a")


@pytest.fixture
def agent_otp_login(flask_client):
    url = get_url_for_resource(AgentOTPLogin)

    def _agent_otp_login(request_body):
        return flask_client.post(url, json=request_body, follow_redirects=True)

    return _agent_otp_login


def test_agent_otp_login__successful(agent_otp_login):
    response = agent_otp_login({"agent_id": AGENT_ID, "otp": "supersecretpassword"})

    assert response.status_code == 200
    assert ACCESS_TOKEN_KEY_NAME in response.json["response"]["user"]
    assert REFRESH_TOKEN_KEY_NAME in response.json["response"]["user"]


@pytest.mark.parametrize(
    "data",
    [
        {},
        [],
        {"otp": ""},
        {"agent_id": AGENT_ID},
        {"agent_id": "", "otp": "supersecretpassword"},
        {"agent_id": "1234", "otp": "supersecretpassword"},
    ],
)
def test_invalid_request(agent_otp_login, data):
    response = agent_otp_login(data)

    assert response.status_code == 400


def test_invalid_json(flask_client):
    url = get_url_for_resource(AgentOTPLogin)
    invalid_json = "{'key1': 'value1', 'key2: 'value2'}"

    response = flask_client.post(url, data=invalid_json, follow_redirects=True)

    assert response.status_code == 400


def test_unauthorized(agent_otp_login):
    # TODO: Update this test when OTP validation is implemented.
    response = agent_otp_login({"agent_id": AGENT_ID, "otp": ""})

    assert response.status_code == 401


def test_unexpected_error(mock_authentication_facade, agent_otp_login):
    mock_authentication_facade.generate_refresh_token.side_effect = Exception("Unexpected error")
    response = agent_otp_login({"agent_id": AGENT_ID, "otp": "password"})

    assert response.status_code == 500
