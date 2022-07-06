import pytest
from marshmallow.exceptions import ValidationError

from common.credentials import CredentialComponentType, Password, Username
from common.credentials.password import PasswordSchema
from common.credentials.username import UsernameSchema

PARAMETRIZED_PARAMETER_NAMES = (
    "credential_component_class, schema_class, credential_component_type, key, value"
)

PARAMETRIZED_PARAMETER_VALUES = [
    (Password, PasswordSchema, CredentialComponentType.PASSWORD, "password", "123456"),
    (Username, UsernameSchema, CredentialComponentType.USERNAME, "username", "test_user"),
]


def build_credential_dict(credential_component_type: CredentialComponentType, key: str, value: str):
    return {"credential_type": credential_component_type.name, key: value}


@pytest.mark.parametrize(PARAMETRIZED_PARAMETER_NAMES, PARAMETRIZED_PARAMETER_VALUES)
def test_credential_component_serialize(
    credential_component_class, schema_class, credential_component_type, key, value
):
    schema = schema_class()
    print(type(schema))
    constructed_object = credential_component_class(value)
    print(type(constructed_object))

    serialized_object = schema.dump(constructed_object)

    assert serialized_object == build_credential_dict(credential_component_type, key, value)


@pytest.mark.parametrize(PARAMETRIZED_PARAMETER_NAMES, PARAMETRIZED_PARAMETER_VALUES)
def test_credential_component_deserialize(
    credential_component_class, schema_class, credential_component_type, key, value
):
    schema = schema_class()
    credential_dict = build_credential_dict(credential_component_type, key, value)
    expected_deserialized_object = credential_component_class(value)

    deserialized_object = credential_component_class(**schema.load(credential_dict))

    assert deserialized_object == expected_deserialized_object


@pytest.mark.parametrize(PARAMETRIZED_PARAMETER_NAMES, PARAMETRIZED_PARAMETER_VALUES)
def test_invalid_credential_type(
    credential_component_class, schema_class, credential_component_type, key, value
):
    invalid_component_dict = build_credential_dict(credential_component_type, key, value)
    invalid_component_dict["credential_type"] = "INVALID"
    schema = schema_class()

    with pytest.raises(ValidationError):
        credential_component_class(**schema.load(invalid_component_dict))


@pytest.mark.parametrize(PARAMETRIZED_PARAMETER_NAMES, PARAMETRIZED_PARAMETER_VALUES)
def test_encorrect_credential_type(
    credential_component_class, schema_class, credential_component_type, key, value
):
    incorrect_component_dict = build_credential_dict(credential_component_type, key, value)
    incorrect_component_dict["credential_type"] = (
        CredentialComponentType.USERNAME.name
        if credential_component_type != CredentialComponentType.USERNAME
        else CredentialComponentType.PASSWORD
    )
    schema = schema_class()

    with pytest.raises(ValidationError):
        credential_component_class(**schema.load(incorrect_component_dict))
