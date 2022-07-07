from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, MutableMapping, Sequence, Tuple

from marshmallow import Schema, fields, post_load, pre_dump

from . import (
    CredentialComponentType,
    InvalidCredentialComponentError,
    InvalidCredentialsError,
    LMHash,
    NTHash,
    Password,
    SSHKeypair,
    Username,
)
from .i_credential_component import ICredentialComponent
from .lm_hash import LMHashSchema
from .nt_hash import NTHashSchema
from .password import PasswordSchema
from .ssh_keypair import SSHKeypairSchema
from .username import UsernameSchema

CREDENTIAL_COMPONENT_TYPE_TO_CLASS = {
    CredentialComponentType.LM_HASH: LMHash,
    CredentialComponentType.NT_HASH: NTHash,
    CredentialComponentType.PASSWORD: Password,
    CredentialComponentType.SSH_KEYPAIR: SSHKeypair,
    CredentialComponentType.USERNAME: Username,
}

CREDENTIAL_COMPONENT_TYPE_TO_CLASS_SCHEMA = {
    CredentialComponentType.LM_HASH: LMHashSchema(),
    CredentialComponentType.NT_HASH: NTHashSchema(),
    CredentialComponentType.PASSWORD: PasswordSchema(),
    CredentialComponentType.SSH_KEYPAIR: SSHKeypairSchema(),
    CredentialComponentType.USERNAME: UsernameSchema(),
}


class CredentialsSchema(Schema):
    # Use fields.List instead of fields.Tuple because marshmallow requires fields.Tuple to have a
    # fixed length.
    identities = fields.List(fields.Mapping())
    secrets = fields.List(fields.Mapping())

    @post_load
    def _make_credentials(
        self, data: MutableMapping, **kwargs: Mapping[str, Any]
    ) -> Mapping[str, Sequence[Mapping[str, Any]]]:
        data["identities"] = tuple(
            [
                CredentialsSchema._build_credential_component(component)
                for component in data["identities"]
            ]
        )
        data["secrets"] = tuple(
            [
                CredentialsSchema._build_credential_component(component)
                for component in data["secrets"]
            ]
        )

        return data

    @staticmethod
    def _build_credential_component(data: Mapping[str, Any]) -> ICredentialComponent:
        try:
            credential_component_type = CredentialComponentType[data["credential_type"]]
        except KeyError as err:
            raise InvalidCredentialsError(f"Unknown credential component type {err}")

        credential_component_class = CREDENTIAL_COMPONENT_TYPE_TO_CLASS[credential_component_type]
        credential_component_schema = CREDENTIAL_COMPONENT_TYPE_TO_CLASS_SCHEMA[
            credential_component_type
        ]

        return credential_component_class(**credential_component_schema.load(data))

    @pre_dump
    def _serialize_credentials(
        self, credentials: Credentials, **kwargs
    ) -> Mapping[str, Sequence[Mapping[str, Any]]]:
        data = {}

        data["identities"] = tuple(
            [
                CredentialsSchema._serialize_credential_component(component)
                for component in credentials.identities
            ]
        )
        data["secrets"] = tuple(
            [
                CredentialsSchema._serialize_credential_component(component)
                for component in credentials.secrets
            ]
        )

        return data

    @staticmethod
    def _serialize_credential_component(
        credential_component: ICredentialComponent,
    ) -> Mapping[str, Any]:
        credential_component_schema = CREDENTIAL_COMPONENT_TYPE_TO_CLASS_SCHEMA[
            credential_component.credential_type
        ]

        return credential_component_schema.dump(credential_component)


@dataclass(frozen=True)
class Credentials:
    identities: Tuple[ICredentialComponent]
    secrets: Tuple[ICredentialComponent]

    @staticmethod
    def from_mapping(credentials: Mapping) -> Credentials:
        try:
            deserialized_data = CredentialsSchema().load(credentials)
            return Credentials(**deserialized_data)
        except (InvalidCredentialsError, InvalidCredentialComponentError) as err:
            raise err
        except Exception as err:
            raise InvalidCredentialsError(str(err))

    @staticmethod
    def from_json(credentials: str) -> Credentials:
        try:
            deserialized_data = CredentialsSchema().loads(credentials)
            return Credentials(**deserialized_data)
        except (InvalidCredentialsError, InvalidCredentialComponentError) as err:
            raise err
        except Exception as err:
            raise InvalidCredentialsError(str(err))

    @staticmethod
    def to_json(credentials: Credentials) -> str:
        return CredentialsSchema().dumps(credentials)
