import pytest

from monkey_island.cc.services.authentication_service.flask_resources.agent_otp import AgentOTP


@pytest.fixture
def make_otp_request(flask_client):
    url = AgentOTP.urls[0]

    def _make_otp_request():
        return flask_client.get(url)

    return _make_otp_request


def test_agent_otp__successful(make_otp_request):
    response = make_otp_request()

    assert response.status_code == 200
    assert response.json["otp"] == "supersecretpassword"
