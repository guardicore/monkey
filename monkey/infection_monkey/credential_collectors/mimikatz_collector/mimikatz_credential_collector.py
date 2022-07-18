import logging
from typing import Sequence

from common.credentials import Credentials, LMHash, NTHash, Password, Username
from infection_monkey.i_puppet import ICredentialCollector
from infection_monkey.model import USERNAME_PREFIX

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
            identity = None

            # Mimikatz picks up users created by the Monkey even if they're successfully deleted
            # since it picks up creds from the registry. The newly created users are not removed
            # from the registry until a reboot of the system, hence this check.
            if win_cred.username and not win_cred.username.startswith(USERNAME_PREFIX):
                identity = Username(win_cred.username)

            if win_cred.password:
                password = Password(win_cred.password)
                all_creds.append(Credentials(identity, password))

            if win_cred.lm_hash:
                lm_hash = LMHash(lm_hash=win_cred.lm_hash)
                all_creds.append(Credentials(identity, lm_hash))

            if win_cred.ntlm_hash:
                ntlm_hash = NTHash(nt_hash=win_cred.ntlm_hash)
                all_creds.append(Credentials(identity, ntlm_hash))

        return all_creds
