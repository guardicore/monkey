from tests.data_for_tests.otp import OTP

from infection_monkey.model import AGENT_OTP_ENVIRONMENT_VARIABLE, InfectionMonkey


def test_get_otp(monkeypatch):
    monkeypatch.setattr("os.environ", {AGENT_OTP_ENVIRONMENT_VARIABLE: OTP})

    assert InfectionMonkey._get_otp() == OTP


def test_get_otp__no_opt(monkeypatch):
    monkeypatch.setattr("os.environ", {AGENT_OTP_ENVIRONMENT_VARIABLE: OTP})

    assert InfectionMonkey._get_otp() == OTP
