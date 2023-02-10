from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr
from tests.data_for_tests.propagation_credentials import (
    CREDENTIALS,
    LM_HASH,
    NT_HASH,
    PASSWORD_1,
    PASSWORD_2,
    PASSWORD_3,
    PRIVATE_KEY,
    PUBLIC_KEY,
    SPECIAL_USERNAME,
    USERNAME,
)

from common.credentials import Credentials, LMHash, NTHash, Password, SSHKeypair, Username
from infection_monkey.propagation_credentials_repository import (
    AggregatingPropagationCredentialsRepository,
)

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
STOLEN_PASSWORD_1 = SecretStr("abcdefg")
STOLEN_PASSWORD_2 = SecretStr("super_secret")
STOLEN_PUBLIC_KEY_1 = "some_public_key_1"
STOLEN_PUBLIC_KEY_2 = "some_public_key_2"
STOLEN_LM_HASH = SecretStr("AAD3B435B51404EEAAD3B435B51404EE")
STOLEN_NT_HASH = SecretStr("C0172DFF622FE29B5327CB79DC12D24C")
STOLEN_PRIVATE_KEY_1 = SecretStr("some_private_key_1")
STOLEN_PRIVATE_KEY_2 = SecretStr("some_private_key_2")
STOLEN_CREDENTIALS = [
    Credentials(
        identity=Username(username=STOLEN_USERNAME_1),
        secret=Password(password=PASSWORD_1),
    ),
    Credentials(
        identity=Username(username=STOLEN_USERNAME_1), secret=Password(password=STOLEN_PASSWORD_1)
    ),
    Credentials(
        identity=Username(username=STOLEN_USERNAME_2),
        secret=SSHKeypair(public_key=STOLEN_PUBLIC_KEY_1, private_key=STOLEN_PRIVATE_KEY_1),
    ),
    Credentials(
        identity=None,
        secret=Password(password=STOLEN_PASSWORD_2),
    ),
    Credentials(
        identity=Username(username=STOLEN_USERNAME_2), secret=LMHash(lm_hash=STOLEN_LM_HASH)
    ),
    Credentials(
        identity=Username(username=STOLEN_USERNAME_2), secret=NTHash(nt_hash=STOLEN_NT_HASH)
    ),
    Credentials(identity=Username(username=STOLEN_USERNAME_3), secret=None),
]

STOLEN_SSH_KEYS_CREDENTIALS = [
    Credentials(
        identity=Username(username=USERNAME),
        secret=SSHKeypair(public_key=STOLEN_PUBLIC_KEY_2, private_key=STOLEN_PRIVATE_KEY_2),
    )
]


@pytest.fixture
def aggregating_credentials_repository() -> AggregatingPropagationCredentialsRepository:
    control_channel = MagicMock()
    control_channel.get_credentials_for_propagation.return_value = CREDENTIALS
    return AggregatingPropagationCredentialsRepository(control_channel)


@pytest.mark.parametrize("key", TRANSFORMED_CONTROL_CHANNEL_CREDENTIALS.keys())
def test_get_credentials_from_repository(aggregating_credentials_repository, key):
    actual_stored_credentials = aggregating_credentials_repository.get_credentials()

    assert actual_stored_credentials[key] == TRANSFORMED_CONTROL_CHANNEL_CREDENTIALS[key]


def test_add_credentials_to_repository(aggregating_credentials_repository):
    aggregating_credentials_repository.add_credentials(STOLEN_CREDENTIALS)
    aggregating_credentials_repository.add_credentials(STOLEN_SSH_KEYS_CREDENTIALS)

    actual_stored_credentials = aggregating_credentials_repository.get_credentials()

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
    credentials_repository = AggregatingPropagationCredentialsRepository(control_channel)

    actual_stored_credentials = credentials_repository.get_credentials()
    print(type(actual_stored_credentials))

    assert "exploit_user_list" in actual_stored_credentials
    assert "exploit_password_list" in actual_stored_credentials
    assert "exploit_ntlm_hash_list" in actual_stored_credentials
    assert "exploit_ssh_keys" in actual_stored_credentials


def test_credentials_obtained_if_propagation_credentials_fails():
    control_channel = MagicMock()
    control_channel.get_credentials_for_propagation.return_value = EMPTY_CHANNEL_CREDENTIALS
    control_channel.get_credentials_for_propagation.side_effect = Exception(
        "No credentials for you!"
    )
    credentials_repository = AggregatingPropagationCredentialsRepository(control_channel)

    credentials = credentials_repository.get_credentials()

    assert credentials is not None
