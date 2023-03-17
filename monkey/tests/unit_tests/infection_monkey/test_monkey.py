import os

import pytest
from tests.data_for_tests.otp import OTP

from infection_monkey.model import AGENT_OTP_ENVIRONMENT_VARIABLE, OTP_FLAG
from infection_monkey.monkey import InfectionMonkey


@pytest.fixture(autouse=True)
def configure_environment_variables(monkeypatch):
    monkeypatch.setenv(AGENT_OTP_ENVIRONMENT_VARIABLE, OTP)
    monkeypatch.setenv(OTP_FLAG, True)


def test_get_otp(monkeypatch):
    assert InfectionMonkey._get_otp() == OTP
    assert AGENT_OTP_ENVIRONMENT_VARIABLE not in os.environ


def test_get_otp__no_otp(monkeypatch):
    monkeypatch.delenv(AGENT_OTP_ENVIRONMENT_VARIABLE)
    with pytest.raises(Exception):
        InfectionMonkey._get_otp()


def test_get_otp__feature_flag_disabled(monkeypatch):
    try:
        monkeypatch.delenv(OTP_FLAG)
    except KeyError:
        pass

    # No need for a constant, this code is testing a feature flag that will be removed.
    assert InfectionMonkey._get_otp() == "PLACEHOLDER_OTP"
