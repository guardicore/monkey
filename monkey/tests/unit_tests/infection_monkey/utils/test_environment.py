import pytest
from monkeytypes import OperatingSystem

from infection_monkey.utils.environment import get_os


def test_get_os__windows(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Windows")
    assert get_os() == OperatingSystem.WINDOWS


def test_get_os__linux(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Linux")
    assert get_os() == OperatingSystem.LINUX


def test_get_os__unsupported(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "")

    with pytest.raises(RuntimeError):
        get_os()
