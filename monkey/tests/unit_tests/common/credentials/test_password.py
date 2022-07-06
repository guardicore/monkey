from copy import deepcopy

import pytest
from marshmallow.exceptions import ValidationError

from common.credentials import CredentialComponentType, Password
from common.credentials.password import PasswordSchema

PASSWORD_VALUE = "123456"
PASSWORD_DICT = {
    "credential_type": CredentialComponentType.PASSWORD.name,
    "password": PASSWORD_VALUE,
}


def test_password_serialize():
    schema = PasswordSchema()
    password = Password(PASSWORD_VALUE)

    serialized_password = schema.dump(password)

    assert serialized_password == PASSWORD_DICT


def test_password_deserialize():
    schema = PasswordSchema()

    password = Password(**schema.load(PASSWORD_DICT))

    assert password.credential_type == CredentialComponentType.PASSWORD
    assert password.password == PASSWORD_VALUE


def test_invalid_credential_type():
    invalid_password_dict = deepcopy(PASSWORD_DICT)
    invalid_password_dict["credential_type"] = "INVALID"
    schema = PasswordSchema()

    with pytest.raises(ValidationError):
        Password(**schema.load(invalid_password_dict))


def test_incorrect_credential_type():
    invalid_password_dict = deepcopy(PASSWORD_DICT)
    invalid_password_dict["credential_type"] = CredentialComponentType.USERNAME.name
    schema = PasswordSchema()

    with pytest.raises(ValidationError):
        Password(**schema.load(invalid_password_dict))
