import pytest

from monkey_island.cc.services.authentication_service.flask_resources.register_agent import RegisterAgent


@pytest.fixture
def register_agent(flask_client):
    url = RegisterAgent.urls[0]

    def _register_agent(request_body):
        return flask_client.post(url, data=request_body, follow_redirects=True)

    return _register_agent


def test_register_agent__successful(register_agent):
    response = register_agent('{"otp": "supersecretpassword"}')

    assert response.status_code == 200
    assert response.json["token"] == "supersecrettoken"


@pytest.mark.parametrize("data", [{}, [], '{"otp": ""}'])
def test_register_agent__failure(register_agent, data):
    response = register_agent(data)

    assert response.status_code == 400
