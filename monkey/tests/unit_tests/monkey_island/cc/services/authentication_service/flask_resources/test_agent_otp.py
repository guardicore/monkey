from http import HTTPStatus
from typing import Callable

import pytest
from tests.data_for_tests.otp import TEST_OTP

from monkey_island.cc.services.authentication_service import IOTPGenerator
from monkey_island.cc.services.authentication_service.flask_resources.agent_otp import AgentOTP


@pytest.fixture
def make_otp_request(flask_client):
    url = AgentOTP.urls[0]

    def _make_otp_request():
        return flask_client.get(url)

    return _make_otp_request


def test_agent_otp__successful(make_otp_request: Callable, mock_otp_generator: IOTPGenerator):
    mock_otp_generator.generate_otp.return_value = TEST_OTP
    response = make_otp_request()

    assert response.status_code == HTTPStatus.OK
    assert response.json["otp"] == TEST_OTP.get_secret_value()
