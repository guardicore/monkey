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

    for credential in credentials["data"]:
        if is_ssh_keypair(credential):
            SECRET_PROCESSORS[CredentialsType.SSH_KEYPAIR](credential, credentials["monkey_guid"])
        else:
            for identity in credential["identities"]:
                IDENTITY_PROCESSORS[identity["credential_type"]](identity)
            for secret in credential["secrets"]:
                SECRET_PROCESSORS[secret["credential_type"]](secret)


def is_ssh_keypair(credential: dict) -> bool:
    return bool(
        filter(
            lambda secret: secret["credential_type"] == CredentialsType.SSH_KEYPAIR,
            credential["secrets"],
        )
    )
