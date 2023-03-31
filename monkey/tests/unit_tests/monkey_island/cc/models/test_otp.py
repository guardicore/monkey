from datetime import datetime, timezone

import pytest

from monkey_island.cc.models import OTP

OTP_DICT = {"otp": "otp", "expiration_time": datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)}
OTP_SIMPLE_DICT = {"otp": "otp", "expiration_time": "2020-01-01T00:00:00+00:00"}


def test_otp__constructor():
    otp = OTP(**OTP_DICT)

    assert otp.otp == OTP_DICT["otp"]
    assert otp.expiration_time == OTP_DICT["expiration_time"]


def test_otp__to_dict():
    otp = OTP(**OTP_DICT)

    assert otp.dict(simplify=True) == OTP_SIMPLE_DICT


def test_otp__immutable():
    otp = OTP(**OTP_DICT)

    with pytest.raises(TypeError):
        otp.otp = "new-otp"


def test_expiration_time__immutable():
    otp = OTP(**OTP_DICT)

    with pytest.raises(TypeError):
        otp.expiration_time = datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
