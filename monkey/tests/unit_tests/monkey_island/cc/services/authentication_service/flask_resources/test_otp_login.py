import pytest

from monkey_island.cc.services.authentication_service.flask_resources.otp_login import OTPLogin


@pytest.fixture
def otp_login(flask_client):
    url = OTPLogin.urls[0]

    def _otp_login(request_body):
        return flask_client.post(url, data=request_body, follow_redirects=True)

    return _otp_login


def test_otp_login__successful(otp_login):
    response = otp_login('{"otp": "supersecretpassword"}')

    assert response.status_code == 200
    assert response.json["token"] == "supersecrettoken"


@pytest.mark.parametrize("data", [{}, [], '{"otp": ""}'])
def test_otp_login__failure(otp_login, data):
    response = otp_login(data)

    assert response.status_code == 400
