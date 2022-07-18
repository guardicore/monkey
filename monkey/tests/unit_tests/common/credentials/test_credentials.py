import json
from itertools import product

import pytest
from tests.data_for_tests.propagation_credentials import (
    LM_HASH,
    NT_HASH,
    PASSWORD_1,
    PRIVATE_KEY,
    PUBLIC_KEY,
    USERNAME,
)

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

IDENTITIES = [Username(USERNAME), None]
IDENTITY_DICTS = [{"credential_type": "USERNAME", "username": USERNAME}, None]

SECRETS = (
    Password(PASSWORD_1),
    LMHash(LM_HASH),
    NTHash(NT_HASH),
    SSHKeypair(PRIVATE_KEY, PUBLIC_KEY),
    None,
)
SECRET_DICTS = [
    {"credential_type": "PASSWORD", "password": PASSWORD_1},
    {"credential_type": "LM_HASH", "lm_hash": LM_HASH},
    {"credential_type": "NT_HASH", "nt_hash": NT_HASH},
    {
        "credential_type": "SSH_KEYPAIR",
        "public_key": PUBLIC_KEY,
        "private_key": PRIVATE_KEY,
    },
    None,
]

CREDENTIALS = [
    Credentials(identity, secret)
    for identity, secret in product(IDENTITIES, SECRETS)
    if not (identity is None and secret is None)
]

CREDENTIALS_DICTS = [
    {"identity": identity, "secret": secret}
    for identity, secret in product(IDENTITY_DICTS, SECRET_DICTS)
    if not (identity is None and secret is None)
]


@pytest.mark.parametrize(
    "credentials, expected_credentials_dict", zip(CREDENTIALS, CREDENTIALS_DICTS)
)
def test_credentials_serialization_json(credentials, expected_credentials_dict):
    serialized_credentials = Credentials.to_json(credentials)

    assert json.loads(serialized_credentials) == expected_credentials_dict


@pytest.mark.parametrize(
    "credentials, expected_credentials_dict", zip(CREDENTIALS, CREDENTIALS_DICTS)
)
def test_credentials_serialization_mapping(credentials, expected_credentials_dict):
    serialized_credentials = Credentials.to_mapping(credentials)

    assert serialized_credentials == expected_credentials_dict


@pytest.mark.parametrize(
    "expected_credentials, credentials_dict", zip(CREDENTIALS, CREDENTIALS_DICTS)
)
def test_credentials_deserialization__from_mapping(expected_credentials, credentials_dict):
    deserialized_credentials = Credentials.from_mapping(credentials_dict)

    assert deserialized_credentials == expected_credentials


@pytest.mark.parametrize(
    "expected_credentials, credentials_dict", zip(CREDENTIALS, CREDENTIALS_DICTS)
)
def test_credentials_deserialization__from_json(expected_credentials, credentials_dict):
    deserialized_credentials = Credentials.from_json(json.dumps(credentials_dict))

    assert deserialized_credentials == expected_credentials


def test_credentials_deserialization__invalid_credentials():
    invalid_data = {"secret": SECRET_DICTS[0], "unknown_key": []}
    with pytest.raises(InvalidCredentialsError):
        Credentials.from_mapping(invalid_data)


def test_credentials_deserialization__invalid_component_type():
    invalid_data = {
        "secret": SECRET_DICTS[0],
        "identity": {"credential_type": "FAKE", "username": "user1"},
    }
    with pytest.raises(InvalidCredentialsError):
        Credentials.from_mapping(invalid_data)


def test_credentials_deserialization__invalid_component():
    invalid_data = {
        "secret": SECRET_DICTS[0],
        "identity": {"credential_type": "USERNAME", "unknown_field": "user1"},
    }
    with pytest.raises(InvalidCredentialComponentError):
        Credentials.from_mapping(invalid_data)


def test_create_credentials__none_none():
    with pytest.raises(InvalidCredentialsError):
        Credentials(None, None)
