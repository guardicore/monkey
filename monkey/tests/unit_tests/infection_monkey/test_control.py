import pytest

from monkey.infection_monkey.control import ControlClient


@pytest.mark.parametrize(
    "is_windows_os,expected_proxy_string",
    [(True, "http://8.8.8.8:45455"), (False, "8.8.8.8:45455")],
)
def test_control_set_proxies(monkeypatch, is_windows_os, expected_proxy_string):
    monkeypatch.setattr("monkey.infection_monkey.control.is_windows_os", lambda: is_windows_os)
    control_client = ControlClient("8.8.8.8:5000")

    control_client.set_proxies(("8.8.8.8", "45455"))

    assert control_client.proxies["https"] == expected_proxy_string
