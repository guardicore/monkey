from copy import deepcopy

import pytest
from marshmallow.exceptions import ValidationError

from common.credentials import CredentialComponentType, Username
from common.credentials.username import UsernameSchema

USERNAME_VALUE = "test_user"
USERNAME_DICT = {
    "credential_type": CredentialComponentType.USERNAME.name,
    "username": USERNAME_VALUE,
}


def test_username_serialize():
    schema = UsernameSchema()
    username = Username(USERNAME_VALUE)

    serialized_username = schema.dump(username)

    assert serialized_username == USERNAME_DICT


def test_username_deserialize():
    schema = UsernameSchema()

    username = Username(**schema.load(USERNAME_DICT))

    assert username.credential_type == CredentialComponentType.USERNAME
    assert username.username == USERNAME_VALUE


def test_invalid_credential_type():
    invalid_username_dict = deepcopy(USERNAME_DICT)
    invalid_username_dict["credential_type"] = "INVALID"
    schema = UsernameSchema()

    with pytest.raises(ValidationError):
        Username(**schema.load(invalid_username_dict))


def test_incorrect_credential_type():
    invalid_username_dict = deepcopy(USERNAME_DICT)
    invalid_username_dict["credential_type"] = CredentialComponentType.PASSWORD.name
    schema = UsernameSchema()

    with pytest.raises(ValidationError):
        Username(**schema.load(invalid_username_dict))
