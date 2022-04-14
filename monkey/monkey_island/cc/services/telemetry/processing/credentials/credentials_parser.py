import logging
from itertools import chain
from typing import Mapping

from common.common_consts.credential_component_type import CredentialComponentType
from monkey_island.cc.models import StolenCredentials

from .credentials import Credentials
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


def parse_credentials(telemetry_dict: Mapping):
    credentials = [
        Credentials.from_mapping(credential, telemetry_dict["monkey_guid"])
        for credential in telemetry_dict["data"]
    ]

    for credential in credentials:
        _store_in_db(credential)
        for cred_comp in chain(credential.identities, credential.secrets):
            credential_type = CredentialComponentType[cred_comp["credential_type"]]
            CREDENTIAL_COMPONENT_PROCESSORS[credential_type](cred_comp, credential)


def _store_in_db(credentials: Credentials):
    stolen_cred_doc = StolenCredentials.from_credentials(credentials)
    stolen_cred_doc.save()
