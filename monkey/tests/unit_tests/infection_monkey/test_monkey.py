import os

import pytest
from tests.data_for_tests.otp import TEST_OTP

from common.common_consts import AGENT_OTP_ENVIRONMENT_VARIABLE
from infection_monkey.monkey import InfectionMonkey


@pytest.fixture(autouse=True)
def configure_environment_variables(monkeypatch):
    monkeypatch.setenv(AGENT_OTP_ENVIRONMENT_VARIABLE, TEST_OTP.get_secret_value())


def test_get_otp(monkeypatch):
    assert InfectionMonkey._get_otp().get_secret_value() == TEST_OTP.get_secret_value()
    assert AGENT_OTP_ENVIRONMENT_VARIABLE not in os.environ


def test_get_otp__no_otp(monkeypatch):
    monkeypatch.delenv(AGENT_OTP_ENVIRONMENT_VARIABLE)
    with pytest.raises(Exception):
        InfectionMonkey._get_otp()
