import logging
from typing import Mapping

from common.common_consts.credential_component_type import CredentialComponentType

from .identities.username_processor import process_username
from .secrets.lm_hash_processor import process_lm_hash
from .secrets.nt_hash_processor import process_nt_hash
from .secrets.password_processor import process_password

logger = logging.getLogger(__name__)

SECRET_PROCESSORS = {
    CredentialComponentType.PASSWORD: process_password,
    CredentialComponentType.NT_HASH: process_nt_hash,
    CredentialComponentType.LM_HASH: process_lm_hash,
}

IDENTITY_PROCESSORS = {
    CredentialComponentType.USERNAME: process_username,
}


def parse_credentials(credentials: Mapping):
    for credential in credentials["data"]:
        for identity in credential["identities"]:
            credential_type = CredentialComponentType[identity["credential_type"]]
            IDENTITY_PROCESSORS[credential_type](identity)
        for secret in credential["secrets"]:
            credential_type = CredentialComponentType[secret["credential_type"]]
            SECRET_PROCESSORS[credential_type](secret)
