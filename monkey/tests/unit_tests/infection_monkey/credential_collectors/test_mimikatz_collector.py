from typing import Sequence

import pytest

from infection_monkey.credential_collectors import (
    LMHash,
    MimikatzCredentialCollector,
    NTHash,
    Password,
    Username,
)
from infection_monkey.credential_collectors.mimikatz_collector.windows_credentials import (
    WindowsCredentials,
)
from infection_monkey.i_puppet import Credentials


def patch_pypykatz(win_creds: [WindowsCredentials], monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.credential_collectors"
        ".mimikatz_collector.pypykatz_handler.get_windows_creds",
        lambda: win_creds,
    )


def collect_credentials() -> Sequence[Credentials]:
    return MimikatzCredentialCollector().collect_credentials()


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
    expected_credentials = Credentials([username], [password])

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
        WindowsCredentials(username="user2", password="secret2", lm_hash="lm_hash"),
    ]
    patch_pypykatz(win_creds, monkeypatch)

    # Expected credentials
    username = Username("user2")
    password = Password("secret2")
    lm_hash = LMHash("lm_hash")
    expected_credentials = Credentials([username], [password, lm_hash])

    collected_credentials = collect_credentials()
    assert len(collected_credentials) == 1
    assert collected_credentials[0] == expected_credentials


def test_pypykatz_result_parsing_no_identities(monkeypatch):
    win_creds = [
        WindowsCredentials(username="", password="", ntlm_hash="ntlm_hash", lm_hash="lm_hash"),
    ]
    patch_pypykatz(win_creds, monkeypatch)

    lm_hash = LMHash("lm_hash")
    nt_hash = NTHash("ntlm_hash")
    expected_credentials = Credentials([], [lm_hash, nt_hash])

    collected_credentials = collect_credentials()
    assert len(collected_credentials) == 1
    assert collected_credentials[0] == expected_credentials
