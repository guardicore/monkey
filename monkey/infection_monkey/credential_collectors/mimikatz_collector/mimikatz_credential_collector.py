import logging
from typing import Sequence

from infection_monkey.credential_collectors import LMHash, NTHash, Password, Username
from infection_monkey.i_puppet.credential_collection import Credentials, ICredentialCollector

from . import pypykatz_handler
from .windows_credentials import WindowsCredentials

logger = logging.getLogger(__name__)


class MimikatzCredentialCollector(ICredentialCollector):

    def collect_credentials(self, options=None) -> Sequence[Credentials]:
        logger.info("Attempting to collect windows credentials with pypykatz.")
        creds = pypykatz_handler.get_windows_creds()
        logger.info(f"Pypykatz gathered {len(creds)} credentials.")
        return MimikatzCredentialCollector._to_credentials(creds)

    @staticmethod
    def _to_credentials(win_creds: Sequence[WindowsCredentials]) -> [Credentials]:
        all_creds = []
        for win_cred in win_creds:
            identities = []
            secrets = []
            if win_cred.username:
                identity = Username(win_cred.username)
                identities.append(identity)

            if win_cred.password:
                password = Password(win_cred.password)
                secrets.append(password)

            if win_cred.lm_hash:
                lm_hash = LMHash(lm_hash=win_cred.lm_hash)
                secrets.append(lm_hash)

            if win_cred.ntlm_hash:
                lm_hash = NTHash(nt_hash=win_cred.ntlm_hash)
                secrets.append(lm_hash)

            if identities != [] or secrets != []:
                all_creds.append(Credentials(identities, secrets))
        return all_creds
