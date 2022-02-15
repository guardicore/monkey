from infection_monkey.credential_collectors import Credentials, SSHKeypair, Username
from infection_monkey.credential_collectors.ssh_collector import SSHCollector


def patch_ssh_handler(ssh_creds, monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.credential_collectors.ssh_collector.ssh_handler.get_ssh_info",
        lambda: ssh_creds,
    )


def test_ssh_credentials_empty_results(monkeypatch):
    patch_ssh_handler([], monkeypatch)
    collected = SSHCollector().collect_credentials()
    assert [] == collected

    ssh_creds = [
        {"name": "", "home_dir": "", "public_key": None, "private_key": None, "known_hosts": None}
    ]
    patch_ssh_handler(ssh_creds, monkeypatch)
    expected = []
    collected = SSHCollector().collect_credentials()
    assert expected == collected


def test_ssh_info_result_parsing(monkeypatch):

    ssh_creds = [
        {
            "name": "ubuntu",
            "home_dir": "/home/ubuntu",
            "public_key": "SomePublicKeyUbuntu",
            "private_key": "ExtremelyGoodPrivateKey",
            "known_hosts": "MuchKnownHosts",
        },
        {
            "name": "mcus",
            "home_dir": "/home/mcus",
            "public_key": "AnotherPublicKey",
            "private_key": "NotSoGoodPrivateKey",
            "known_hosts": None,
        },
        {
            "name": "",
            "home_dir": "/",
            "public_key": None,
            "private_key": None,
            "known_hosts": "VeryGoodHosts1",
        },
    ]
    patch_ssh_handler(ssh_creds, monkeypatch)

    # Expected credentials
    username = Username("ubuntu")
    username2 = Username("mcus")

    ssh_keypair1 = SSHKeypair(
        {
            "public_key": "SomePublicKeyUbuntu",
            "private_key": "ExtremelyGoodPrivateKey",
            "known_hosts": "MuchKnownHosts",
        }
    )
    ssh_keypair2 = SSHKeypair(
        {"public_key": "AnotherPublicKey", "private_key": "NotSoGoodPrivateKey"}
    )
    ssh_keypair3 = SSHKeypair({"known_hosts": "VeryGoodHosts"})

    expected = [
        Credentials(identities=[username], secrets=[ssh_keypair1]),
        Credentials(identities=[username2], secrets=[ssh_keypair2]),
        Credentials(identities=[], secrets=[ssh_keypair3]),
    ]
    collected = SSHCollector().collect_credentials()
    assert expected == collected
