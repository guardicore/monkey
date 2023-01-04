from typing import List
from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr
from tests.data_for_tests.propagation_credentials import CREDENTIALS, PASSWORD_1, USERNAME

from common.credentials import Credentials, LMHash, NTHash, Password, SSHKeypair, Username
from infection_monkey.propagation_credentials_repository import PropagationCredentialsRepository

EMPTY_CHANNEL_CREDENTIALS: List[Credentials] = []

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
def propagation_credentials_repository() -> PropagationCredentialsRepository:
    control_channel = MagicMock()
    control_channel.get_credentials_for_propagation.return_value = CREDENTIALS
    return PropagationCredentialsRepository(control_channel)


def test_get_credentials__retrieves_from_control_channel(propagation_credentials_repository):
    actual_stored_credentials = propagation_credentials_repository.get_credentials()

    assert set(actual_stored_credentials) == set(CREDENTIALS)


def test_add_credentials(propagation_credentials_repository):
    propagation_credentials_repository.add_credentials(STOLEN_CREDENTIALS)
    propagation_credentials_repository.add_credentials(STOLEN_SSH_KEYS_CREDENTIALS)

    actual_stored_credentials = propagation_credentials_repository.get_credentials()

    assert set(actual_stored_credentials) == set(
        STOLEN_CREDENTIALS + STOLEN_SSH_KEYS_CREDENTIALS + CREDENTIALS
    )


def test_credentials_obtained_if_propagation_credentials_fails():
    control_channel = MagicMock()
    control_channel.get_credentials_for_propagation.return_value = EMPTY_CHANNEL_CREDENTIALS
    control_channel.get_credentials_for_propagation.side_effect = Exception(
        "No credentials for you!"
    )
    credentials_repository = PropagationCredentialsRepository(control_channel)

    credentials = credentials_repository.get_credentials()

    assert credentials is not None
