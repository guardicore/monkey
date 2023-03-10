import pytest

from monkey_island.cc.services.authentication_service.flask_resources.agent_otp_login import (
    AgentOTPLogin,
)


@pytest.fixture
def agent_otp_login(flask_client):
    url = AgentOTPLogin.urls[0]

    def _agent_otp_login(request_body):
        return flask_client.post(url, data=request_body, follow_redirects=True)

    return _agent_otp_login


def test_agent_otp_login__successful(agent_otp_login):
    response = agent_otp_login('{"otp": "supersecretpassword"}')

    assert response.status_code == 200
    assert response.json["token"] == "supersecrettoken"


@pytest.mark.parametrize("data", [{}, [], '{"otp": ""}'])
def test_agent_otp_login__failure(agent_otp_login, data):
    response = agent_otp_login(data)

    assert response.status_code == 400
