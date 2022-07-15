import logging
from typing import Mapping, Sequence

from common.credentials import CredentialComponentType, Credentials

logger = logging.getLogger(__name__)


def format_creds_for_reporting(credentials: Sequence[Credentials]) -> Sequence[Mapping]:
    logger.info("Stolen creds generated for reporting")

    formatted_creds = []
    cred_type_dict = {
        CredentialComponentType.PASSWORD: "Clear Password",
        CredentialComponentType.LM_HASH: "LM hash",
        CredentialComponentType.NT_HASH: "NTLM hash",
        CredentialComponentType.SSH_KEYPAIR: "Clear SSH private key",
    }
    for cred in credentials:
        for secret_type in cred.secrets:
            if secret_type.credential_type not in cred_type_dict:
                continue
            username = _get_username(cred)
            cred_row = {
                "username": username,
                "_type": secret_type.credential_type.name,
                "type": cred_type_dict[secret_type.credential_type],
            }
            if cred_row not in formatted_creds:
                formatted_creds.append(cred_row)
    return formatted_creds


def _get_username(credentials: Credentials) -> str:
    return credentials.identities[0].username if credentials.identities else ""
