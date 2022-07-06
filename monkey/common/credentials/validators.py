import re
from typing import Type

from marshmallow import Schema, validate

from . import ICredentialComponent

_ntlm_hash_regex = re.compile(r"^[a-fA-F0-9]{32}$")
ntlm_hash_validator = validate.Regexp(regex=_ntlm_hash_regex)


class InvalidCredentialComponent(Exception):
    def __init__(self, credential_component_class: Type[ICredentialComponent], message: str):
        self._credential_component_name = credential_component_class.__name__
        self._message = message

    def __str__(self) -> str:
        return (
            f"Cannot construct a {self._credential_component_name} object with the supplied, "
            f"invalid data: {self._message}"
        )


def credential_component_validator(schema: Schema, credential_component: ICredentialComponent):
    """
    Validate a credential component

    :param schema: A marshmallow schema used for validating the component
    :param credential_component: A credential component to be validated
    :raises InvalidCredentialComponent: if the credential_component contains invalid data
    """
    try:
        serialized_data = schema.dump(credential_component)

        # This will raise an exception if the object is invalid. Calling this in __post__init()
        # makes it impossible to construct an invalid object
        schema.load(serialized_data)
    except Exception as err:
        raise InvalidCredentialComponent(credential_component.__class__, err)
