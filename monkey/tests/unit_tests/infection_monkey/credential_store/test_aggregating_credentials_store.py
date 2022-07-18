from unittest.mock import MagicMock

import pytest
from tests.data_for_tests.propagation_credentials import (
    LM_HASH,
    NT_HASH,
    PASSWORD_1,
    PASSWORD_2,
    PASSWORD_3,
    PRIVATE_KEY,
    PROPAGATION_CREDENTIALS,
    PUBLIC_KEY,
    SPECIAL_USERNAME,
    USERNAME,
)

from common.credentials import Credentials, LMHash, NTHash, Password, SSHKeypair, Username
from infection_monkey.credential_store import AggregatingCredentialsStore

CONTROL_CHANNEL_CREDENTIALS = PROPAGATION_CREDENTIALS
TRANSFORMED_CONTROL_CHANNEL_CREDENTIALS = {
    "exploit_user_list": {USERNAME, SPECIAL_USERNAME},
    "exploit_password_list": {PASSWORD_1, PASSWORD_2, PASSWORD_3},
    "exploit_lm_hash_list": {LM_HASH},
    "exploit_ntlm_hash_list": {NT_HASH},
    "exploit_ssh_keys": [{"public_key": PUBLIC_KEY, "private_key": PRIVATE_KEY}],
}

EMPTY_CHANNEL_CREDENTIALS = []

STOLEN_USERNAME_1 = "user1"
STOLEN_USERNAME_2 = "user2"
STOLEN_USERNAME_3 = "user3"
STOLEN_PASSWORD_1 = "abcdefg"
STOLEN_PASSWORD_2 = "super_secret"
STOLEN_PUBLIC_KEY_1 = "some_public_key_1"
STOLEN_PUBLIC_KEY_2 = "some_public_key_2"
STOLEN_LM_HASH = "AAD3B435B51404EEAAD3B435B51404EE"
STOLEN_NT_HASH = "C0172DFF622FE29B5327CB79DC12D24C"
STOLEN_PRIVATE_KEY_1 = "some_private_key_1"
STOLEN_PRIVATE_KEY_2 = "some_private_key_2"
STOLEN_CREDENTIALS = [
    Credentials(
        identity=Username(STOLEN_USERNAME_1),
        secret=Password(PASSWORD_1),
    ),
    Credentials(identity=Username(STOLEN_USERNAME_1), secret=Password(STOLEN_PASSWORD_1)),
    Credentials(
        identity=Username(STOLEN_USERNAME_2),
        secret=SSHKeypair(public_key=STOLEN_PUBLIC_KEY_1, private_key=STOLEN_PRIVATE_KEY_1),
    ),
    Credentials(
        identity=None,
        secret=Password(STOLEN_PASSWORD_2),
    ),
    Credentials(identity=Username(STOLEN_USERNAME_2), secret=LMHash(STOLEN_LM_HASH)),
    Credentials(identity=Username(STOLEN_USERNAME_2), secret=NTHash(STOLEN_NT_HASH)),
    Credentials(identity=Username(STOLEN_USERNAME_3), secret=None),
]

STOLEN_SSH_KEYS_CREDENTIALS = [
    Credentials(
        Username(USERNAME),
        SSHKeypair(public_key=STOLEN_PUBLIC_KEY_2, private_key=STOLEN_PRIVATE_KEY_2),
    )
]


@pytest.fixture
def aggregating_credentials_store() -> AggregatingCredentialsStore:
    control_channel = MagicMock()
    control_channel.get_credentials_for_propagation.return_value = CONTROL_CHANNEL_CREDENTIALS
    return AggregatingCredentialsStore(control_channel)


@pytest.mark.parametrize("key", TRANSFORMED_CONTROL_CHANNEL_CREDENTIALS.keys())
def test_get_credentials_from_store(aggregating_credentials_store, key):
    actual_stored_credentials = aggregating_credentials_store.get_credentials()

    assert actual_stored_credentials[key] == TRANSFORMED_CONTROL_CHANNEL_CREDENTIALS[key]


def test_add_credentials_to_store(aggregating_credentials_store):
    aggregating_credentials_store.add_credentials(STOLEN_CREDENTIALS)
    aggregating_credentials_store.add_credentials(STOLEN_SSH_KEYS_CREDENTIALS)

    actual_stored_credentials = aggregating_credentials_store.get_credentials()

    assert actual_stored_credentials["exploit_user_list"] == set(
        [
            USERNAME,
            SPECIAL_USERNAME,
            STOLEN_USERNAME_1,
            STOLEN_USERNAME_2,
            STOLEN_USERNAME_3,
        ]
    )
    assert actual_stored_credentials["exploit_password_list"] == set(
        [
            PASSWORD_1,
            PASSWORD_2,
            PASSWORD_3,
            STOLEN_PASSWORD_1,
            STOLEN_PASSWORD_2,
        ]
    )
    assert actual_stored_credentials["exploit_lm_hash_list"] == set([LM_HASH, STOLEN_LM_HASH])
    assert actual_stored_credentials["exploit_ntlm_hash_list"] == set([NT_HASH, STOLEN_NT_HASH])

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
