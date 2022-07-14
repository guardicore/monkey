import logging
from typing import Mapping, Sequence

from common.credentials import CredentialComponentType
from monkey_island.cc.models import StolenCredentials

logger = logging.getLogger(__name__)


def get_stolen_creds() -> Sequence[Mapping]:
    stolen_creds = _fetch_from_db()
    stolen_creds = _format_creds_for_reporting(stolen_creds)

    logger.info("Stolen creds generated for reporting")
    return stolen_creds


def _fetch_from_db() -> Sequence[StolenCredentials]:
    return list(StolenCredentials.objects())


def _format_creds_for_reporting(credentials: Sequence[StolenCredentials]):
    formatted_creds = []
    cred_type_dict = {
        CredentialComponentType.PASSWORD.name: "Clear Password",
        CredentialComponentType.LM_HASH.name: "LM hash",
        CredentialComponentType.NT_HASH.name: "NTLM hash",
        CredentialComponentType.SSH_KEYPAIR.name: "Clear SSH private key",
    }

    for cred in credentials:
        for secret_type in cred.secrets:
            if secret_type not in cred_type_dict:
                continue
            username = _get_username(cred)
            cred_row = {
                "username": username,
                "_type": secret_type,
                "type": cred_type_dict[secret_type],
                "origin": cred.monkey.hostname,
            }
            if cred_row not in formatted_creds:
                formatted_creds.append(cred_row)
    return formatted_creds


def _get_username(credentials: StolenCredentials) -> str:
    return credentials.identities[0]["username"] if credentials.identities else ""
