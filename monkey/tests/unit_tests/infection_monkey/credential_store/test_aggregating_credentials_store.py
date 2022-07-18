from unittest.mock import MagicMock

import pytest

from common.credentials import Credentials, Password, SSHKeypair, Username
from infection_monkey.credential_store import AggregatingCredentialsStore

CONTROL_CHANNEL_CREDENTIALS = {
    "exploit_user_list": ["Administrator", "root", "user1"],
    "exploit_password_list": ["123456", "123456789", "password", "root"],
    "exploit_lm_hash_list": ["aasdf23asd1fdaasadasdfas"],
    "exploit_ntlm_hash_list": ["asdfadvxvsdftw3e3421234123412", "qw4trklxklvznksbhasd1231"],
    "exploit_ssh_keys": [
        {"public_key": "some_public_key", "private_key": "some_private_key"},
        {
            "public_key": "ssh-ed25519 AAAAC3NzEIFaJ7xH+Yoxd\n",
            "private_key": "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BdHIAAAAGYXjl0j66VAKruPEKjS3A=\n"
            "-----END OPENSSH PRIVATE KEY-----\n",
        },
    ],
}

EMPTY_CHANNEL_CREDENTIALS = {
    "exploit_user_list": [],
    "exploit_password_list": [],
    "exploit_lm_hash_list": [],
    "exploit_ntlm_hash_list": [],
    "exploit_ssh_keys": [],
}

TEST_CREDENTIALS = [
    Credentials(
        identity=Username("user1"),
        secret=Password("root"),
    ),
    Credentials(identity=Username("user1"), secret=Password("abcdefg")),
    Credentials(
        identity=Username("user3"),
        secret=SSHKeypair(public_key="some_public_key_1", private_key="some_private_key_1"),
    ),
]

SSH_KEYS_CREDENTIALS = [
    Credentials(
        Username("root"),
        SSHKeypair(public_key="some_public_key", private_key="some_private_key"),
    )
]


@pytest.fixture
def aggregating_credentials_store() -> AggregatingCredentialsStore:
    control_channel = MagicMock()
    control_channel.get_credentials_for_propagation.return_value = CONTROL_CHANNEL_CREDENTIALS
    return AggregatingCredentialsStore(control_channel)


def test_get_credentials_from_store(aggregating_credentials_store):
    actual_stored_credentials = aggregating_credentials_store.get_credentials()

    assert actual_stored_credentials["exploit_user_list"] == set(
        CONTROL_CHANNEL_CREDENTIALS["exploit_user_list"]
    )
    assert actual_stored_credentials["exploit_password_list"] == set(
        CONTROL_CHANNEL_CREDENTIALS["exploit_password_list"]
    )
    assert actual_stored_credentials["exploit_ntlm_hash_list"] == set(
        CONTROL_CHANNEL_CREDENTIALS["exploit_ntlm_hash_list"]
    )

    for ssh_keypair in actual_stored_credentials["exploit_ssh_keys"]:
        assert ssh_keypair in CONTROL_CHANNEL_CREDENTIALS["exploit_ssh_keys"]


def test_add_credentials_to_store(aggregating_credentials_store):
    aggregating_credentials_store.add_credentials(TEST_CREDENTIALS)
    aggregating_credentials_store.add_credentials(SSH_KEYS_CREDENTIALS)

    actual_stored_credentials = aggregating_credentials_store.get_credentials()

    assert actual_stored_credentials["exploit_user_list"] == set(
        [
            "Administrator",
            "root",
            "user1",
            "user3",
        ]
    )
    assert actual_stored_credentials["exploit_password_list"] == set(
        [
            "123456",
            "123456789",
            "abcdefg",
            "password",
            "root",
        ]
    )

    assert len(actual_stored_credentials["exploit_ssh_keys"]) == 3


def test_all_keys_if_credentials_empty():
    control_channel = MagicMock()
    control_channel.get_credentials_for_propagation.return_value = EMPTY_CHANNEL_CREDENTIALS
    credentials_store = AggregatingCredentialsStore(control_channel)

    actual_stored_credentials = credentials_store.get_credentials()
    print(type(actual_stored_credentials))

    assert "exploit_user_list" in actual_stored_credentials
    assert "exploit_password_list" in actual_stored_credentials
    assert "exploit_ntlm_hash_list" in actual_stored_credentials
    assert "exploit_ssh_keys" in actual_stored_credentials
