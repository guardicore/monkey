import pytest

from monkey.infection_monkey.control import ControlClient

PROXY_FOUND = ("8.8.8.8", "45455")


@pytest.mark.parametrize("is_windows_os", [True, False])
def test_control_set_proxies(monkeypatch, is_windows_os):
    monkeypatch.setattr("monkey.infection_monkey.control.is_windows_os", lambda: is_windows_os)
    control_client = ControlClient()

    control_client.set_proxies(PROXY_FOUND)

    if is_windows_os:
        assert control_client.proxies["https"].startswith("http://")
    else:
        assert control_client.proxies["https"].startswith(PROXY_FOUND[0])
