from unittest.mock import MagicMock

import pytest

from common.credentials import Credentials, SSHKeypair, Username
from common.event_queue import IEventQueue
from infection_monkey.credential_collectors import SSHCredentialCollector


@pytest.fixture
def patch_telemetry_messenger():
    return MagicMock()


@pytest.fixture
def mock_event_queue():
    return MagicMock(spec=IEventQueue)


def patch_ssh_handler(ssh_creds, monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.credential_collectors.ssh_collector.ssh_handler.get_ssh_info",
        lambda _: ssh_creds,
    )


def patch_guid(monkeypatch):
    monkeypatch.setattr("infection_monkey.config.GUID", "1-2-3-4-5-6")


@pytest.mark.parametrize(
    "ssh_creds", [([{"name": "", "home_dir": "", "public_key": None, "private_key": None}]), ([])]
)
def test_ssh_credentials_empty_results(
    monkeypatch, ssh_creds, patch_telemetry_messenger, mock_event_queue
):
    patch_ssh_handler(ssh_creds, monkeypatch)
    collected = SSHCredentialCollector(
        patch_telemetry_messenger, mock_event_queue
    ).collect_credentials()
    assert not collected
    mock_event_queue.publish.assert_called_once()


def test_ssh_info_result_parsing(monkeypatch, patch_telemetry_messenger, mock_event_queue):

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
            "public_key": "PubKey",
            "private_key": "PrivKey",
        },
    ]
    patch_ssh_handler(ssh_creds, monkeypatch)

    # Expected credentials
    username = Username("ubuntu")
    username2 = Username("mcus")
    username3 = Username("guest")

    ssh_keypair1 = SSHKeypair("ExtremelyGoodPrivateKey", "SomePublicKeyUbuntu")
    ssh_keypair2 = SSHKeypair("", "AnotherPublicKey")
    ssh_keypair3 = SSHKeypair("PrivKey", "PubKey")

    expected = [
        Credentials(identity=username, secret=ssh_keypair1),
        Credentials(identity=username2, secret=ssh_keypair2),
        Credentials(identity=username3, secret=None),
        Credentials(identity=None, secret=ssh_keypair3),
    ]
    collected = SSHCredentialCollector(
        patch_telemetry_messenger, mock_event_queue
    ).collect_credentials()
    assert expected == collected
    mock_event_queue.publish.assert_called_once()
