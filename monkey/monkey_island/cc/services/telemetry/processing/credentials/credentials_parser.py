import logging

from infection_monkey.i_puppet import CredentialType

from .identities.username_processor import process_username
from .secrets.lm_hash_processor import process_lm_hash
from .secrets.nt_hash_processor import process_nt_hash
from .secrets.password_processor import process_password
from .secrets.ssh_key_processor import process_ssh_key

logger = logging.getLogger(__name__)

SECRET_PROCESSORS = {
    CredentialType.PASSWORD: process_password,
    CredentialType.NT_HASH: process_nt_hash,
    CredentialType.LM_HASH: process_lm_hash,
    CredentialType.SSH_KEYPAIR: process_ssh_key,
}

IDENTITY_PROCESSORS = {
    CredentialType.USERNAME: process_username,
}


def parse_credentials(credentials: dict):
    for credential in credentials["credentials"]:
        if is_ssh_keypair(credentials):
            IDENTITY_PROCESSORS[CredentialType.SSH_KEYPAIR](credential, credentials["monkey_guid"])
        else:
            for identity in credential["identities"]:
                IDENTITY_PROCESSORS[identity["type"]](identity)
            for secret in credential["secrets"]:
                SECRET_PROCESSORS[secret["type"]](secret)


def is_ssh_keypair(credentials: dict) -> bool:
    return bool(
        filter(credentials["secrets"], lambda secret: secret["type"] == CredentialType.SSH_KEYPAIR)
    )
