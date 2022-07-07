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
USER2 = "test_user_2"
PASSWORD = "12435"
LM_HASH = "AEBD4DE384C7EC43AAD3B435B51404EE"
NT_HASH = "7A21990FCD3D759941E45C490F143D5F"
PUBLIC_KEY = "MY_PUBLIC_KEY"
PRIVATE_KEY = "MY_PRIVATE_KEY"

CREDENTIALS_DICT = {
    "identities": [
        {"credential_type": "USERNAME", "username": USER1},
        {"credential_type": "USERNAME", "username": USER2},
    ],
    "secrets": [
        {"credential_type": "PASSWORD", "password": PASSWORD},
        {"credential_type": "LM_HASH", "lm_hash": LM_HASH},
        {"credential_type": "NT_HASH", "nt_hash": NT_HASH},
        {
            "credential_type": "SSH_KEYPAIR",
            "public_key": PUBLIC_KEY,
            "private_key": PRIVATE_KEY,
        },
    ],
}

CREDENTIALS_JSON = json.dumps(CREDENTIALS_DICT)

IDENTITIES = (Username(USER1), Username(USER2))
SECRETS = (
    Password(PASSWORD),
    LMHash(LM_HASH),
    NTHash(NT_HASH),
    SSHKeypair(PRIVATE_KEY, PUBLIC_KEY),
)
CREDENTIALS_OBJECT = Credentials(IDENTITIES, SECRETS)


def test_credentials_serialization_json():
    serialized_credentials = Credentials.to_json(CREDENTIALS_OBJECT)

    assert json.loads(serialized_credentials) == CREDENTIALS_DICT


def test_credentials_deserialization__from_mapping():
    deserialized_credentials = Credentials.from_mapping(CREDENTIALS_DICT)

    assert deserialized_credentials == CREDENTIALS_OBJECT


def test_credentials_deserialization__from_json():
    deserialized_credentials = Credentials.from_json(CREDENTIALS_JSON)

    assert deserialized_credentials == CREDENTIALS_OBJECT


def test_credentials_deserialization__invalid_credentials():
    invalid_data = {"secrets": [], "unknown_key": []}
    with pytest.raises(InvalidCredentialsError):
        Credentials.from_mapping(invalid_data)


def test_credentials_deserialization__invalid_component_type():
    invalid_data = {"secrets": [], "identities": [{"credential_type": "FAKE", "username": "user1"}]}
    with pytest.raises(InvalidCredentialsError):
        Credentials.from_mapping(invalid_data)


def test_credentials_deserialization__invalid_component():
    invalid_data = {
        "secrets": [],
        "identities": [{"credential_type": "USERNAME", "unknown_field": "user1"}],
    }
    with pytest.raises(InvalidCredentialComponentError):
        Credentials.from_mapping(invalid_data)
