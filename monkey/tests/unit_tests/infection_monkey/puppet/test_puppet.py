import threading
from unittest.mock import MagicMock

from infection_monkey.puppet.plugin_type import PluginType
from infection_monkey.puppet.puppet import Puppet


def test_puppet_run_payload_success(monkeypatch):
    p = Puppet()

    payload = MagicMock()
    payload_name = "PayloadOne"

    p.load_plugin(payload, payload_name, PluginType.PAYLOAD)
    p.run_payload(payload_name, {}, threading.Event())

    payload.return_value.run_payload.assert_called_once()


def test_puppet_run_multiple_payloads(monkeypatch):
    p = Puppet()

    payload_1 = MagicMock()
    payload1_name = "PayloadOne"

    payload_2 = MagicMock()
    payload2_name = "PayloadTwo"

    payload_3 = MagicMock()
    payload3_name = "PayloadThree"

    p.load_plugin(payload_1, payload1_name, PluginType.PAYLOAD)
    p.load_plugin(payload_2, payload2_name, PluginType.PAYLOAD)
    p.load_plugin(payload_3, payload3_name, PluginType.PAYLOAD)

    p.run_payload(payload1_name, {}, threading.Event())
    payload_1.return_value.run_payload.assert_called_once()

    p.run_payload(payload2_name, {}, threading.Event())
    payload_2.return_value.run_payload.assert_called_once()

    p.run_payload(payload3_name, {}, threading.Event())
    payload_3.return_value.run_payload.assert_called_once()
