from typing import List

from infection_monkey.credential_collectors import (
    Credentials,
    ICredentialCollector,
    NTHashes,
    Password,
    Username,
)

from . import pypykatz_handler
from .windows_credentials import WindowsCredentials


class MimikatzCredentialCollector(ICredentialCollector):
    def collect_credentials(self) -> List[Credentials]:
        creds = pypykatz_handler.get_windows_creds()
        return MimikatzCredentialCollector.to_credentials(creds)

    @staticmethod
    def to_credentials(win_creds: List[WindowsCredentials]) -> [Credentials]:
        all_creds = []
        for win_cred in win_creds:
            creds_obj = Credentials(identities=[], secrets=[])
            if win_cred.username:
                identity = Username(win_cred.username)
                creds_obj.identities.append(identity)

            if win_cred.password:
                password = Password(win_cred.password)
                creds_obj.secrets.append(password)

            if win_cred.lm_hash or win_cred.ntlm_hash:
                hashes = NTHashes(ntlm_hash=win_cred.ntlm_hash, lm_hash=win_cred.lm_hash)
                creds_obj.secrets.append(hashes)

            if creds_obj.identities != [] or creds_obj.secrets != []:
                all_creds.append(creds_obj)

        return all_creds
