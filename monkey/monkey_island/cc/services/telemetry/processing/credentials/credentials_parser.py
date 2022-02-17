import logging

from common.common_consts.credentials_type import CredentialsType

from .identities.username_processor import process_username
from .secrets.lm_hash_processor import process_lm_hash
from .secrets.nt_hash_processor import process_nt_hash
from .secrets.password_processor import process_password
from .secrets.ssh_key_processor import process_ssh_key

logger = logging.getLogger(__name__)

SECRET_PROCESSORS = {
    CredentialsType.PASSWORD: process_password,
    CredentialsType.NT_HASH: process_nt_hash,
    CredentialsType.LM_HASH: process_lm_hash,
    CredentialsType.SSH_KEYPAIR: process_ssh_key,
}

IDENTITY_PROCESSORS = {
    CredentialsType.USERNAME: process_username,
}


def parse_credentials(credentials: dict):
    for credential in credentials["credentials"]:
        if is_ssh_keypair(credentials):
            IDENTITY_PROCESSORS[CredentialsType.SSH_KEYPAIR](credential, credentials["monkey_guid"])
        else:
            for identity in credential["identities"]:
                IDENTITY_PROCESSORS[identity["type"]](identity)
            for secret in credential["secrets"]:
                SECRET_PROCESSORS[secret["type"]](secret)


def is_ssh_keypair(credentials: dict) -> bool:
    return bool(
        filter(credentials["secrets"], lambda secret: secret["type"] == CredentialsType.SSH_KEYPAIR)
    )
