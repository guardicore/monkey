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
        windows_credentials = pypykatz_handler.get_windows_creds()
        logger.info(f"Pypykatz gathered {len(windows_credentials)} credentials.")
        return MimikatzCredentialCollector._to_credentials(windows_credentials)

    @staticmethod
    def _to_credentials(windows_credentials: Sequence[WindowsCredentials]) -> Sequence[Credentials]:
        credentials = []
        for wc in windows_credentials:
            identity = None

            # Mimikatz picks up users created by the Monkey even if they're successfully deleted
            # since it picks up creds from the registry. The newly created users are not removed
            # from the registry until a reboot of the system, hence this check.
            if wc.username and not wc.username.startswith(USERNAME_PREFIX):
                identity = Username(wc.username)

            if wc.password:
                password = Password(wc.password)
                credentials.append(Credentials(identity, password))

            if wc.lm_hash:
                lm_hash = LMHash(lm_hash=wc.lm_hash)
                credentials.append(Credentials(identity, lm_hash))

            if wc.ntlm_hash:
                ntlm_hash = NTHash(nt_hash=wc.ntlm_hash)
                credentials.append(Credentials(identity, ntlm_hash))

        return credentials
