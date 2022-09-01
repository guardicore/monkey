import logging
from typing import Mapping, Sequence

from common.credentials import Credentials, LMHash, NTHash, Password, SSHKeypair

logger = logging.getLogger(__name__)


def format_creds_for_reporting(credentials: Sequence[Credentials]) -> Sequence[Mapping]:
    logger.info("Stolen creds generated for reporting")

    formatted_creds = []
    cred_type_dict = {
        Password: "Clear Password",
        LMHash: "LM hash",
        NTHash: "NTLM hash",
        SSHKeypair: "Clear SSH private key",
    }
    for cred in credentials:
        secret = cred.secret
        if secret is None:
            continue

        if type(secret) not in cred_type_dict:
            continue
        username = _get_username(cred)
        cred_row = {
            "username": username,
            "type": cred_type_dict[type(secret)],
        }
        if cred_row not in formatted_creds:
            formatted_creds.append(cred_row)
    return formatted_creds


def _get_username(credentials: Credentials) -> str:
    return credentials.identity.username if credentials.identity else ""
