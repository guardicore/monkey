from unittest.mock import MagicMock

import pytest

from common.credentials import Credentials, SSHKeypair, Username
from common.event_queue import IAgentEventQueue
from common.types import AgentID
from infection_monkey.credential_collectors import SSHCredentialCollector

AGENT_ID = AgentID("ed077054-a316-479a-a99d-75bb378c0a6e")


def patch_ssh_handler(ssh_creds, monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.credential_collectors.ssh_collector.ssh_handler.get_ssh_info",
        lambda _, __: ssh_creds,
    )


@pytest.mark.parametrize(
    "ssh_creds", [([{"name": "", "home_dir": "", "public_key": None, "private_key": None}]), ([])]
)
def test_ssh_credentials_empty_results(monkeypatch, ssh_creds):
    patch_ssh_handler(ssh_creds, monkeypatch)
    collected = SSHCredentialCollector(MagicMock(spec=IAgentEventQueue), AGENT_ID).run()
    assert not collected


def test_ssh_info_result_parsing(monkeypatch):
    ssh_creds = [
        {
            "name": "ubuntu",
            "home_dir": "/home/ubuntu",
            "public_key": "SomePublicKeyUbuntu",
            "private_key": "ExtremelyGoodPrivateKey",
        },
        {
            "name": "mcus",
            "home_dir": "/home/mcus",
            "public_key": "AnotherPublicKey",
            "private_key": None,
        },
        {"name": "guest", "home_dir": "/", "public_key": None, "private_key": None},
        {
            "name": "",
            "home_dir": "/home/mcus",
            "public_key": None,
            "private_key": "PrivKey",
        },
    ]
    patch_ssh_handler(ssh_creds, monkeypatch)

    # Expected credentials
    username = Username(username="ubuntu")
    username2 = Username(username="mcus")
    username3 = Username(username="guest")

    ssh_keypair1 = SSHKeypair(
        private_key="ExtremelyGoodPrivateKey", public_key="SomePublicKeyUbuntu"
    )
    ssh_keypair2 = SSHKeypair(private_key="", public_key="AnotherPublicKey")
    ssh_keypair3 = SSHKeypair(private_key="PrivKey", public_key=None)

    expected = [
        Credentials(identity=username, secret=ssh_keypair1),
        Credentials(identity=username2, secret=ssh_keypair2),
        Credentials(identity=username3, secret=None),
        Credentials(identity=None, secret=ssh_keypair3),
    ]
    collected = SSHCredentialCollector(MagicMock(spec=IAgentEventQueue), AGENT_ID).run()
    assert expected == collected
