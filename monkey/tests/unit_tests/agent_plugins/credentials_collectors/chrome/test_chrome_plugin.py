import threading
from unittest.mock import MagicMock

import pytest
from agent_plugins.credentials_collectors.chrome.src.plugin import Plugin

from common.credentials import Credentials, Password, Username
from common.event_queue import IAgentEventPublisher
from common.types import AgentID
from infection_monkey.i_puppet import TargetHost

AGENT_ID = AgentID("ed077054-a316-479a-a99d-75bb378c0a6e")

CREDENTIALS = [
    Credentials(
        identity=Username(username="some_username"), secret=Password(password="some_password")
    )
]


@pytest.fixture
def target_host():
    return TargetHost(ip="1.1.1.1")


class ExceptionCallable:
    def run(self, interrupt):
        raise Exception()


class MockCallable:
    def run(self):
        return CREDENTIALS


@pytest.mark.parametrize(
    "exception_callable",
    [
        ExceptionCallable,
        lambda *_: ExceptionCallable(),
    ],
)
def test_chrome_plugin__builder_exception(monkeypatch, target_host, exception_callable):
    monkeypatch.setattr(
        "agent_plugins.credentials_collectors.chrome.src.plugin.build_chrome_credentials_collector",
        lambda *_: exception_callable(),
    )
    chrome_plugin = Plugin(
        agent_id=AGENT_ID, agent_event_publisher=MagicMock(spec=IAgentEventPublisher)
    )

    actual_credentials = chrome_plugin.run(
        host=target_host, options={}, interrupt=threading.Event()
    )

    assert actual_credentials == []


def test_chrome_plugin__credential_collector(monkeypatch, target_host):
    monkeypatch.setattr(
        "agent_plugins.credentials_collectors.chrome.src.plugin.build_chrome_credentials_collector",
        lambda *_: MockCallable,
    )
    chrome_plugin = Plugin(
        agent_id=AGENT_ID, agent_event_publisher=MagicMock(spec=IAgentEventPublisher)
    )

    actual_credentials = chrome_plugin.run(
        host=target_host, options={}, interrupt=threading.Event()
    )

    assert actual_credentials == CREDENTIALS
