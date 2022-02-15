from infection_monkey.credential_collectors import Credentials, LMHash, NTHash, Password, Username
from infection_monkey.credential_collectors.mimikatz_collector.mimikatz_cred_collector import (
    MimikatzCredentialCollector,
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


def test_empty_results(monkeypatch):
    win_creds = [WindowsCredentials(username="", password="", ntlm_hash="", lm_hash="")]
    patch_pypykatz(win_creds, monkeypatch)
    expected = []
    collected = MimikatzCredentialCollector().collect_credentials()
    assert expected == collected

    patch_pypykatz([], monkeypatch)
    collected = MimikatzCredentialCollector().collect_credentials()
    assert [] == collected


def test_pypykatz_result_parsing(monkeypatch):
    win_creds = [
        WindowsCredentials(username="user", password="secret", ntlm_hash="", lm_hash=""),
        WindowsCredentials(username="", password="", ntlm_hash="ntlm_hash", lm_hash="lm_hash"),
        WindowsCredentials(username="user", password="secret", ntlm_hash="", lm_hash=""),
        WindowsCredentials(username="user2", password="secret2", lm_hash="lm_hash"),
    ]
    patch_pypykatz(win_creds, monkeypatch)

    # Expected credentials
    username = Username("user")
    username2 = Username("user2")
    password = Password("secret")
    password2 = Password("secret2")
    nt_hash = NTHash(nt_hash="ntlm_hash")
    lm_hash = LMHash(lm_hash="lm_hash")

    expected = [
        Credentials(identities=[username], secrets=[password]),
        Credentials(identities=[], secrets=[lm_hash, nt_hash]),
        Credentials(identities=[username], secrets=[password]),
        Credentials(identities=[username2], secrets=[password2, lm_hash]),
    ]
    collected = MimikatzCredentialCollector().collect_credentials()
    assert expected == collected
