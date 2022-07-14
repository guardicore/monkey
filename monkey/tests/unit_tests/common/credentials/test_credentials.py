import copy
import json

import pytest

from common.credentials import (
    Credentials,
    InvalidCredentialComponentError,
    InvalidCredentialsError,
    LMHash,
    NTHash,
    Password,
    SSHKeypair,
    Username,
)

USER1 = "test_user_1"
PASSWORD = "12435"
LM_HASH = "AEBD4DE384C7EC43AAD3B435B51404EE"
NT_HASH = "7A21990FCD3D759941E45C490F143D5F"
PUBLIC_KEY = "MY_PUBLIC_KEY"
PRIVATE_KEY = "MY_PRIVATE_KEY"

CREDENTIALS_DICT = {
    "identity": {"credential_type": "USERNAME", "username": USER1},
    "secret": {},
}

IDENTITY = Username(USER1)
SECRETS = (
    Password(PASSWORD),
    LMHash(LM_HASH),
    NTHash(NT_HASH),
    SSHKeypair(PRIVATE_KEY, PUBLIC_KEY),
)

SECRETS_DICTS = [
    {"credential_type": "PASSWORD", "password": PASSWORD},
    {"credential_type": "LM_HASH", "lm_hash": LM_HASH},
    {"credential_type": "NT_HASH", "nt_hash": NT_HASH},
    {
        "credential_type": "SSH_KEYPAIR",
        "public_key": PUBLIC_KEY,
        "private_key": PRIVATE_KEY,
    },
]


@pytest.mark.parametrize("secret, expected_secret", zip(SECRETS, SECRETS_DICTS))
def test_credentials_serialization_json(secret, expected_secret):
    expected_credentials = copy.copy(CREDENTIALS_DICT)
    expected_credentials["secret"] = expected_secret
    c = Credentials(IDENTITY, secret)

    serialized_credentials = Credentials.to_json(c)

    assert json.loads(serialized_credentials) == expected_credentials


@pytest.mark.parametrize("secret, expected_secret", zip(SECRETS, SECRETS_DICTS))
def test_credentials_serialization_mapping(secret, expected_secret):
    expected_credentials = copy.copy(CREDENTIALS_DICT)
    expected_credentials["secret"] = expected_secret
    c = Credentials(IDENTITY, secret)

    serialized_credentials = Credentials.to_mapping(c)

    assert serialized_credentials == expected_credentials


@pytest.mark.parametrize("secret, secret_dict", zip(SECRETS, SECRETS_DICTS))
def test_credentials_deserialization__from_mapping(secret, secret_dict):
    expected_credentials = Credentials(IDENTITY, secret)
    credentials_dict = copy.copy(CREDENTIALS_DICT)
    credentials_dict["secret"] = secret_dict

    deserialized_credentials = Credentials.from_mapping(credentials_dict)

    assert deserialized_credentials == expected_credentials


@pytest.mark.parametrize("secret, secret_dict", zip(SECRETS, SECRETS_DICTS))
def test_credentials_deserialization__from_json(secret, secret_dict):
    expected_credentials = Credentials(IDENTITY, secret)
    credentials_dict = copy.copy(CREDENTIALS_DICT)
    credentials_dict["secret"] = secret_dict

    deserialized_credentials = Credentials.from_json(json.dumps(credentials_dict))

    assert deserialized_credentials == expected_credentials


def test_credentials_deserialization__invalid_credentials():
    invalid_data = {"secret": SECRETS_DICTS[0], "unknown_key": []}
    with pytest.raises(InvalidCredentialsError):
        Credentials.from_mapping(invalid_data)


def test_credentials_deserialization__invalid_component_type():
    invalid_data = {
        "secret": SECRETS_DICTS[0],
        "identity": {"credential_type": "FAKE", "username": "user1"},
    }
    with pytest.raises(InvalidCredentialsError):
        Credentials.from_mapping(invalid_data)


def test_credentials_deserialization__invalid_component():
    invalid_data = {
        "secret": SECRETS_DICTS[0],
        "identity": {"credential_type": "USERNAME", "unknown_field": "user1"},
    }
    with pytest.raises(InvalidCredentialComponentError):
        Credentials.from_mapping(invalid_data)
