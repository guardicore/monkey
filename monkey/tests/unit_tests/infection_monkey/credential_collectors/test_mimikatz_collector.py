from typing import Sequence
from unittest.mock import MagicMock, Mock

import pytest
from pubsub.core import Publisher

from common.credentials import Credentials, LMHash, NTHash, Password, Username
from common.event_queue import IEventQueue, PyPubSubEventQueue
from common.events import AbstractEvent
from infection_monkey.credential_collectors import MimikatzCredentialCollector
from infection_monkey.credential_collectors.mimikatz_collector.mimikatz_credential_collector import (
    MIMIKATZ_CREDENTIAL_COLLECTOR_TAG,
    MIMIKATZ_EVENT_TAGS,
    T1003_ATTACK_TECHNIQUE_TAG,
    T1005_ATTACK_TECHNIQUE_TAG,
)
from infection_monkey.credential_collectors.mimikatz_collector.windows_credentials import (
    WindowsCredentials,
)


def patch_pypykatz(win_creds: [WindowsCredentials], monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.credential_collectors"
        ".mimikatz_collector.pypykatz_handler.get_windows_creds",
        lambda: win_creds,
    )


def collect_credentials() -> Sequence[Credentials]:
    mock_event_queue = MagicMock(spec=IEventQueue)
    return MimikatzCredentialCollector(mock_event_queue).collect_credentials()


@pytest.mark.parametrize(
    "win_creds", [([WindowsCredentials(username="", password="", ntlm_hash="", lm_hash="")]), ([])]
)
def test_empty_results(monkeypatch, win_creds):
    patch_pypykatz(win_creds, monkeypatch)
    collected_credentials = collect_credentials()
    assert not collected_credentials


def test_pypykatz_result_parsing(monkeypatch):
    win_creds = [WindowsCredentials(username="user", password="secret", ntlm_hash="", lm_hash="")]
    patch_pypykatz(win_creds, monkeypatch)

    username = Username("user")
    password = Password("secret")
    expected_credentials = Credentials(username, password)

    collected_credentials = collect_credentials()
    assert len(collected_credentials) == 1
    assert collected_credentials[0] == expected_credentials


def test_pypykatz_result_parsing_duplicates(monkeypatch):
    win_creds = [
        WindowsCredentials(username="user", password="secret", ntlm_hash="", lm_hash=""),
        WindowsCredentials(username="user", password="secret", ntlm_hash="", lm_hash=""),
    ]
    patch_pypykatz(win_creds, monkeypatch)

    collected_credentials = collect_credentials()
    assert len(collected_credentials) == 2


def test_pypykatz_result_parsing_defaults(monkeypatch):
    win_creds = [
        WindowsCredentials(
            username="user2", password="secret2", lm_hash="0182BD0BD4444BF8FC83B5D9042EED2E"
        ),
    ]
    patch_pypykatz(win_creds, monkeypatch)

    # Expected credentials
    username = Username("user2")
    password = Password("secret2")
    lm_hash = LMHash("0182BD0BD4444BF8FC83B5D9042EED2E")
    expected_credentials = [Credentials(username, password), Credentials(username, lm_hash)]

    collected_credentials = collect_credentials()
    assert len(collected_credentials) == 2
    assert collected_credentials == expected_credentials


def test_pypykatz_result_parsing_no_identities(monkeypatch):
    win_creds = [
        WindowsCredentials(
            username="",
            password="",
            ntlm_hash="E9F85516721DDC218359AD5280DB4450",
            lm_hash="0182BD0BD4444BF8FC83B5D9042EED2E",
        ),
    ]
    patch_pypykatz(win_creds, monkeypatch)

    lm_hash = LMHash("0182BD0BD4444BF8FC83B5D9042EED2E")
    nt_hash = NTHash("E9F85516721DDC218359AD5280DB4450")
    expected_credentials = [Credentials(None, lm_hash), Credentials(None, nt_hash)]

    collected_credentials = collect_credentials()
    assert len(collected_credentials) == 2
    assert collected_credentials == expected_credentials


def test_pypykatz_result_parsing_no_secrets(monkeypatch):
    username = "user3"
    win_creds = [
        WindowsCredentials(
            username=username,
            password="",
            ntlm_hash="",
            lm_hash="",
        ),
    ]
    patch_pypykatz(win_creds, monkeypatch)

    expected_credentials = [Credentials(Username(username), None)]

    collected_credentials = collect_credentials()
    assert len(collected_credentials) == 1
    assert collected_credentials == expected_credentials


@pytest.fixture
def event_queue() -> IEventQueue:
    return PyPubSubEventQueue(Publisher())


def test_pypykatz_credentials_stolen_event_published(monkeypatch, event_queue):
    def subscriber(event: AbstractEvent):
        subscriber.call_count += 1
        subscriber.call_tags |= event.tags

    subscriber.call_count = 0
    subscriber.call_tags = set()

    event_queue.subscribe_tag(MIMIKATZ_CREDENTIAL_COLLECTOR_TAG, subscriber)
    event_queue.subscribe_tag(T1003_ATTACK_TECHNIQUE_TAG, subscriber)
    event_queue.subscribe_tag(T1005_ATTACK_TECHNIQUE_TAG, subscriber)

    mimikatz_credential_collector = MimikatzCredentialCollector(event_queue)
    monkeypatch.setattr(
        "infection_monkey.credential_collectors.mimikatz_collector.pypykatz_handler", Mock()
    )
    mimikatz_credential_collector.collect_credentials()

    assert subscriber.call_count == 3
    assert subscriber.call_tags == MIMIKATZ_EVENT_TAGS
