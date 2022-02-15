from typing import Iterable

from infection_monkey.credential_collectors import (
    Credentials,
    ICredentialCollector,
    LMHash,
    NTHash,
    Password,
    Username,
)
from . import pypykatz_handler
from .windows_credentials import WindowsCredentials


class MimikatzCredentialCollector(ICredentialCollector):
    def collect_credentials(self, options=None) -> Iterable[Credentials]:
        creds = pypykatz_handler.get_windows_creds()
        return MimikatzCredentialCollector._to_credentials(creds)

    @staticmethod
    def _to_credentials(win_creds: Iterable[WindowsCredentials]) -> [Credentials]:
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
