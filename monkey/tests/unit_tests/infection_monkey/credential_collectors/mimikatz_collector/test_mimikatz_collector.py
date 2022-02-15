from infection_monkey.credential_collectors import LMHash, NTHash, Password, Username
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
    win_creds = [WindowsCredentials(username="user", password="secret", ntlm_hash="", lm_hash="")]
    patch_pypykatz(win_creds, monkeypatch)

    # Expected credentials
    username = Username("user")
    password = Password("secret")

    collected = MimikatzCredentialCollector().collect_credentials()
    assert len(list(collected)) == 1
    assert list(collected)[0].identities[0].__dict__ == username.__dict__
    assert list(collected)[0].secrets[0].__dict__ == password.__dict__


def test_pypykatz_result_parsing_duplicates(monkeypatch):
    win_creds = [
        WindowsCredentials(username="user", password="secret", ntlm_hash="", lm_hash=""),
        WindowsCredentials(username="user", password="secret", ntlm_hash="", lm_hash=""),
    ]
    patch_pypykatz(win_creds, monkeypatch)

    collected = MimikatzCredentialCollector().collect_credentials()
    assert len(list(collected)) == 2


def test_pypykatz_result_parsing_defaults(monkeypatch):
    win_creds = [
        WindowsCredentials(username="user2", password="secret2", lm_hash="lm_hash"),
    ]
    patch_pypykatz(win_creds, monkeypatch)

    # Expected credentials
    username = Username("user2")
    password = Password("secret2")
    lm_hash = LMHash("lm_hash")

    collected = MimikatzCredentialCollector().collect_credentials()
    assert list(collected)[0].identities[0].__dict__ == username.__dict__
    assert list(collected)[0].secrets[0].__dict__ == password.__dict__
    assert list(collected)[0].secrets[1].__dict__ == lm_hash.__dict__


def test_pypykatz_result_parsing_no_identities(monkeypatch):
    win_creds = [
        WindowsCredentials(username="", password="", ntlm_hash="ntlm_hash", lm_hash="lm_hash"),
    ]
    patch_pypykatz(win_creds, monkeypatch)

    # Expected credentials
    nt_hash = NTHash("ntlm_hash")
    lm_hash = LMHash("lm_hash")

    collected = MimikatzCredentialCollector().collect_credentials()
    assert list(collected)[0].secrets[0].__dict__ == lm_hash.__dict__
    assert list(collected)[0].secrets[1].__dict__ == nt_hash.__dict__
