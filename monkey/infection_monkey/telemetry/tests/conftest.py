import pytest

from infection_monkey.control import ControlClient


@pytest.fixture
def spy_send_telemetry(monkeypatch):
    def _spy_send_telemetry(telem_category, data):
        _spy_send_telemetry.telem_category = telem_category
        _spy_send_telemetry.data = data

    _spy_send_telemetry.telem_category = None
    _spy_send_telemetry.data = None
    monkeypatch.setattr(ControlClient, 'send_telemetry', _spy_send_telemetry)
    return _spy_send_telemetry
