from tests.data_for_tests.otp import OTP

from infection_monkey.model import AGENT_OTP_ENVIRONMENT_VARIABLE, OTP_FLAG
from infection_monkey.monkey import InfectionMonkey


def test_get_otp(monkeypatch):
    monkeypatch.setattr("os.environ", {AGENT_OTP_ENVIRONMENT_VARIABLE: OTP})
    monkeypatch.setenv(OTP_FLAG, True)

    assert InfectionMonkey._get_otp() == OTP


def test_get_otp__no_opt(monkeypatch):
    monkeypatch.setattr("os.environ", {AGENT_OTP_ENVIRONMENT_VARIABLE: OTP})
    monkeypatch.setenv(OTP_FLAG, True)

    assert InfectionMonkey._get_otp() == OTP


def test_get_otp__feature_flag_disabled(monkeypatch):
    monkeypatch.setattr("os.environ", {AGENT_OTP_ENVIRONMENT_VARIABLE: OTP})
    try:
        monkeypatch.delenv(OTP_FLAG)
    except KeyError:
        pass

    # No need for a constant, this code is testing a feature flag that will be removed.
    assert InfectionMonkey._get_otp() == "PLACEHOLDER_OTP"
