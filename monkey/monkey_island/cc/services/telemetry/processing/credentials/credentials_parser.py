import logging
from itertools import chain
from typing import Mapping

from common.credentials import CredentialComponentType, Credentials
from monkey_island.cc.repository import ICredentialsRepository

from .identities.username_processor import process_username
from .secrets.lm_hash_processor import process_lm_hash
from .secrets.nt_hash_processor import process_nt_hash
from .secrets.password_processor import process_password
from .secrets.ssh_key_processor import process_ssh_key

logger = logging.getLogger(__name__)

CREDENTIAL_COMPONENT_PROCESSORS = {
    CredentialComponentType.LM_HASH: process_lm_hash,
    CredentialComponentType.NT_HASH: process_nt_hash,
    CredentialComponentType.PASSWORD: process_password,
    CredentialComponentType.SSH_KEYPAIR: process_ssh_key,
    CredentialComponentType.USERNAME: process_username,
}


class CredentialsParser:
    """
    This class parses and stores telemetry credentials.
    """

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    def __call__(self, telemetry_dict):
        self._parse_credentials(telemetry_dict)

    def _parse_credentials(self, telemetry_dict: Mapping):
        credentials = [
            Credentials.from_mapping(credential) for credential in telemetry_dict["data"]
        ]
        self._credentials_repository.save_stolen_credentials(credentials)

        for credential in credentials:
            for cred_comp in chain(credential.identities, credential.secrets):
                credential_type = CredentialComponentType[cred_comp["credential_type"]]
                CREDENTIAL_COMPONENT_PROCESSORS[credential_type](cred_comp, credential)
