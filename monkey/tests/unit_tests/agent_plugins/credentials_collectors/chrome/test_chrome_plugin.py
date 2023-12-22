import threading
from unittest.mock import MagicMock

from agent_plugins.credentials_collectors.chrome.src.plugin import Plugin
from monkeytypes import AgentID, Credentials, Password, Username
from tests.utils import get_reference_to_exception_raising_function

from common.event_queue import IAgentEventPublisher

AGENT_ID = AgentID("ed077054-a316-479a-a99d-75bb378c0a6e")

CREDENTIALS = [
    Credentials(
        identity=Username(username="some_username"), secret=Password(password="some_password")
    )
]


class ExceptionCallable:
    def run(self, interrupt):
        raise_exception = get_reference_to_exception_raising_function(Exception)
        raise_exception()


class MockCallable:
    def run(self):
        return CREDENTIALS


def test_chrome_plugin__build_exception(monkeypatch):
    monkeypatch.setattr(
        "agent_plugins.credentials_collectors.chrome.src.plugin.build_chrome_credentials_collector",
        get_reference_to_exception_raising_function(Exception),
    )
    chrome_plugin = Plugin(
        agent_id=AGENT_ID,
        agent_event_publisher=MagicMock(spec=IAgentEventPublisher),
        local_machine_info=MagicMock(),
    )

    actual_credentials = chrome_plugin.run(options={}, interrupt=threading.Event())

    assert actual_credentials == []


def test_chrome_plugin__run_exception(monkeypatch):
    monkeypatch.setattr(
        "agent_plugins.credentials_collectors.chrome.src.plugin.build_chrome_credentials_collector",
        lambda *_: ExceptionCallable,
    )
    chrome_plugin = Plugin(
        agent_id=AGENT_ID,
        agent_event_publisher=MagicMock(spec=IAgentEventPublisher),
        local_machine_info=MagicMock(),
    )

    actual_credentials = chrome_plugin.run(options={}, interrupt=threading.Event())

    assert actual_credentials == []


def test_chrome_plugin__credential_collector(monkeypatch):
    monkeypatch.setattr(
        "agent_plugins.credentials_collectors.chrome.src.plugin.build_chrome_credentials_collector",
        lambda *_: MockCallable,
    )
    chrome_plugin = Plugin(
        agent_id=AGENT_ID,
        agent_event_publisher=MagicMock(spec=IAgentEventPublisher),
        local_machine_info=MagicMock(),
    )

    actual_credentials = chrome_plugin.run(options={}, interrupt=threading.Event())

    assert actual_credentials == CREDENTIALS
