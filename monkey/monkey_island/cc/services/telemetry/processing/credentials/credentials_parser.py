import logging
from typing import Mapping

from common.common_consts.credential_component_type import CredentialComponentType

from .credentials import Credentials
from .identities.username_processor import process_username
from .secrets.lm_hash_processor import process_lm_hash
from .secrets.nt_hash_processor import process_nt_hash
from .secrets.password_processor import process_password
from .secrets.ssh_key_processor import process_ssh_key

logger = logging.getLogger(__name__)

SECRET_PROCESSORS = {
    CredentialComponentType.PASSWORD: process_password,
    CredentialComponentType.NT_HASH: process_nt_hash,
    CredentialComponentType.LM_HASH: process_lm_hash,
    CredentialComponentType.SSH_KEYPAIR: process_ssh_key,
}

IDENTITY_PROCESSORS = {
    CredentialComponentType.USERNAME: process_username,
}


def parse_credentials(telemetry_dict: Mapping):
    credentials = [
        Credentials.from_dict(credential, telemetry_dict["monkey_guid"])
        for credential in telemetry_dict["data"]
    ]

    for credential in credentials:
        for identity in credential.identities:
            credential_type = CredentialComponentType[identity["credential_type"]]
            IDENTITY_PROCESSORS[credential_type](identity, credential)
        for secret in credential.secrets:
            credential_type = CredentialComponentType[secret["credential_type"]]
            SECRET_PROCESSORS[credential_type](secret, credential)
