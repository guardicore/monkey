import pytest

from common import OperatingSystem
from infection_monkey.utils.environment import get_os


def test_get_os__windows(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Windows")
    assert get_os() == OperatingSystem.WINDOWS


def test_get_os__linux(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Linux")
    assert get_os() == OperatingSystem.LINUX


@pytest.mark.parametrize("os", ["Darwin", "Java"])
def test_get_os__any(monkeypatch, os):
    monkeypatch.setattr("platform.system", lambda: os)
    assert get_os() == OperatingSystem.ANY


def test_get_os__unsupported(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "")

    with pytest.raises(RuntimeError):
        get_os()
