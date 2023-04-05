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
    url = get_url_for_resource(AgentOTPLogin, agent_id=str(AGENT_ID))

    def _agent_otp_login(request_body):
        return flask_client.post(url, data=request_body, follow_redirects=True)

    return _agent_otp_login


def test_agent_otp_login__successful(agent_otp_login):
    response = agent_otp_login('{"otp": "supersecretpassword"}')

    assert response.status_code == 200
    assert ACCESS_TOKEN_KEY_NAME in response.json["response"]["user"]
    assert REFRESH_TOKEN_KEY_NAME in response.json["response"]["user"]


@pytest.mark.parametrize("data", [{}, [], '{"otp": ""}'])
def test_agent_otp_login__failure(agent_otp_login, data):
    response = agent_otp_login(data)

    assert response.status_code == 400
