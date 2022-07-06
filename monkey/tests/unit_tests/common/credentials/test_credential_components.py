from typing import Any, Mapping

import pytest
from marshmallow.exceptions import ValidationError

from common.credentials import CredentialComponentType, LMHash, NTHash, Password, Username
from common.credentials.lm_hash import LMHashSchema
from common.credentials.nt_hash import NTHashSchema
from common.credentials.password import PasswordSchema
from common.credentials.username import UsernameSchema

PARAMETRIZED_PARAMETER_NAMES = (
    "credential_component_class, schema_class, credential_component_type, credential_component_data"
)

PARAMETRIZED_PARAMETER_VALUES = [
    (Username, UsernameSchema, CredentialComponentType.USERNAME, {"username": "test_user"}),
    (Password, PasswordSchema, CredentialComponentType.PASSWORD, {"password": "123456"}),
    (
        LMHash,
        LMHashSchema,
        CredentialComponentType.LM_HASH,
        {"lm_hash": "E52CAC67419A9A224A3B108F3FA6CB6D"},
    ),
    (
        NTHash,
        NTHashSchema,
        CredentialComponentType.NT_HASH,
        {"nt_hash": "E52CAC67419A9A224A3B108F3FA6CB6D"},
    ),
]


INVALID_COMPONENT_DATA = {
    CredentialComponentType.USERNAME: ({"username": None}, {"username": 1}, {"username": 2.0}),
    CredentialComponentType.PASSWORD: ({"password": None}, {"password": 1}, {"password": 2.0}),
    CredentialComponentType.LM_HASH: (
        {"lm_hash": None},
        {"lm_hash": 1},
        {"lm_hash": 2.0},
        {"lm_hash": "0123456789012345678901234568901"},
        {"lm_hash": "E52GAC67419A9A224A3B108F3FA6CB6D"},
    ),
    CredentialComponentType.NT_HASH: (
        {"nt_hash": None},
        {"nt_hash": 1},
        {"nt_hash": 2.0},
        {"nt_hash": "0123456789012345678901234568901"},
        {"nt_hash": "E52GAC67419A9A224A3B108F3FA6CB6D"},
    ),
}


def build_component_dict(
    credential_component_type: CredentialComponentType, credential_component_data: Mapping[str, Any]
):
    return {"credential_type": credential_component_type.name, **credential_component_data}


@pytest.mark.parametrize(PARAMETRIZED_PARAMETER_NAMES, PARAMETRIZED_PARAMETER_VALUES)
def test_credential_component_serialize(
    credential_component_class, schema_class, credential_component_type, credential_component_data
):
    schema = schema_class()
    constructed_object = credential_component_class(**credential_component_data)

    serialized_object = schema.dump(constructed_object)

    assert serialized_object == build_component_dict(
        credential_component_type, credential_component_data
    )


@pytest.mark.parametrize(PARAMETRIZED_PARAMETER_NAMES, PARAMETRIZED_PARAMETER_VALUES)
def test_credential_component_deserialize(
    credential_component_class, schema_class, credential_component_type, credential_component_data
):
    schema = schema_class()
    credential_dict = build_component_dict(credential_component_type, credential_component_data)
    expected_deserialized_object = credential_component_class(**credential_component_data)

    deserialized_object = credential_component_class(**schema.load(credential_dict))

    assert deserialized_object == expected_deserialized_object


@pytest.mark.parametrize(PARAMETRIZED_PARAMETER_NAMES, PARAMETRIZED_PARAMETER_VALUES)
def test_invalid_credential_type(
    credential_component_class, schema_class, credential_component_type, credential_component_data
):
    invalid_component_dict = build_component_dict(
        credential_component_type, credential_component_data
    )
    invalid_component_dict["credential_type"] = "INVALID"
    schema = schema_class()

    with pytest.raises(ValidationError):
        credential_component_class(**schema.load(invalid_component_dict))


@pytest.mark.parametrize(PARAMETRIZED_PARAMETER_NAMES, PARAMETRIZED_PARAMETER_VALUES)
def test_encorrect_credential_type(
    credential_component_class, schema_class, credential_component_type, credential_component_data
):
    incorrect_component_dict = build_component_dict(
        credential_component_type, credential_component_data
    )
    incorrect_component_dict["credential_type"] = (
        CredentialComponentType.USERNAME.name
        if credential_component_type != CredentialComponentType.USERNAME
        else CredentialComponentType.PASSWORD
    )
    schema = schema_class()

    with pytest.raises(ValidationError):
        credential_component_class(**schema.load(incorrect_component_dict))


@pytest.mark.parametrize(PARAMETRIZED_PARAMETER_NAMES, PARAMETRIZED_PARAMETER_VALUES)
def test_invalid_values(
    credential_component_class, schema_class, credential_component_type, credential_component_data
):
    schema = schema_class()

    for invalid_component_data in INVALID_COMPONENT_DATA[credential_component_type]:
        component_dict = build_component_dict(credential_component_type, invalid_component_data)
        with pytest.raises(ValidationError):
            credential_component_class(**schema.load(component_dict))
