from unittest import TestCase

from infection_monkey.system_info.windows_cred_collector.pypykatz_handler import \
    _get_creds_from_pypykatz_session


class TestPypykatzHandler(TestCase):
    # Made up credentials, but structure of dict should be roughly the same
    PYPYKATZ_SESSION = {
        'authentication_id': 555555, 'session_id': 3, 'username': 'Monkey',
        'domainname': 'ReAlDoMaIn', 'logon_server': 'ReAlDoMaIn',
        'logon_time': '2020-06-02T04:53:45.256562+00:00',
        'sid': 'S-1-6-25-260123139-3611579848-5589493929-3021', 'luid': 123086,
        'msv_creds': [
            {'username': 'monkey', 'domainname': 'ReAlDoMaIn',
             'NThash': b'1\xb7<Y\xd7\xe0\xc0\x89\xc01\xd6\xcf\xe0\xd1j\xe9', 'LMHash': None,
             'SHAHash': b'\x18\x90\xaf\xd8\x07\t\xda9\xa3\xee^kK\r2U\xbf\xef\x95`'}],
        'wdigest_creds': [
            {'credtype': 'wdigest', 'username': 'monkey', 'domainname': 'ReAlDoMaIn',
             'password': 'canyoufindme', 'luid': 123086}],
        'ssp_creds': [{'credtype': 'wdigest', 'username': 'monkey123', 'domainname': 'ReAlDoMaIn',
                       'password': 'canyoufindme123', 'luid': 123086}],
        'livessp_creds': [{'credtype': 'wdigest', 'username': 'monk3y', 'domainname': 'ReAlDoMaIn',
                           'password': 'canyoufindm3', 'luid': 123086}],
        'dpapi_creds': [
            {'credtype': 'dpapi', 'key_guid': '9123-123ae123de4-121239-3123-421f',
             'masterkey': '6e81d0cfd5e9ec083cfbdaf4d25b9cc9cc6b72947f5e80920034d1275d8613532025975e'
                          'f051e891c30e6e9af6db54500fedfed1c968389bf6262c77fbaa68c9',
             'sha1_masterkey': 'bbdabc3cd2f6bcbe3e2cee6ce4ce4cebcef4c6da', 'luid': 123086},
            {'credtype': 'dpapi', 'key_guid': '9123-123ae123de4-121239-3123-421f',
             'masterkey': '6e81d0cfd5e9ec083cfbdaf4d25b9cc9cc6b72947f5e80920034d1275d8613532025975e'
                          'f051e891c30e6e9af6db54500fedfed1c968389bf6262c77fbaa68c9',
             'sha1_masterkey': 'bbdabc3cd2f6bcbe3e2cee6ce4ce4cebcef4c6da', 'luid': 123086},
            {'credtype': 'dpapi', 'key_guid': '9123-123ae123de4-121239-3123-421f',
             'masterkey': '6e81d0cfd5e9ec083cfbdaf4d25b9cc9cc6b72947f5e80920034d1275d8613532025975e'
                          'f051e891c30e6e9af6db54500fedfed1c968389bf6262c77fbaa68c9',
             'sha1_masterkey': 'bbdabc3cd2f6bcbe3e2cee6ce4ce4cebcef4c6da', 'luid': 123086},
            {'credtype': 'dpapi', 'key_guid': '9123-123ae123de4-121239-3123-421f',
             'masterkey': '6e81d0cfd5e9ec083cfbdaf4d25b9cc9cc6b72947f5e80920034d1275d8613532025975e'
                          'f051e891c30e6e9af6db54500fedfed1c968389bf6262c77fbaa68c9',
             'sha1_masterkey': 'bbdabc3cd2f6bcbe3e2cee6ce4ce4cebcef4c6da', 'luid': 123086},
            {'credtype': 'dpapi', 'key_guid': '9123-123ae123de4-121239-3123-421f'}],
        'kerberos_creds': [
            {'credtype': 'kerberos', 'username': 'monkey_kerb', 'password': None, 'domainname': 'ReAlDoMaIn',
             'luid': 123086, 'tickets': []}],
        'credman_creds': [
            {'credtype': 'credman', 'username': 'monkey', 'domainname': 'monkey.ad.monkey.com',
             'password': 'canyoufindme2', 'luid': 123086},
            {'credtype': 'credman', 'username': 'monkey@monkey.com', 'domainname': 'moneky.monkey.com',
             'password': 'canyoufindme1', 'luid': 123086},
            {'credtype': 'credman', 'username': 'test', 'domainname': 'test.test.ts', 'password': 'canyoufindit',
             'luid': 123086}],
        'tspkg_creds': []}

    def test__get_creds_from_pypykatz_session(self):
        results = _get_creds_from_pypykatz_session(TestPypykatzHandler.PYPYKATZ_SESSION)

        test_dicts = [{'username': 'monkey',
                       'ntlm_hash': '31b73c59d7e0c089c031d6cfe0d16ae9',
                       'password': '',
                       'lm_hash': ''},
                      {'username': 'monkey',
                       'ntlm_hash': '',
                       'password': 'canyoufindme',
                       'lm_hash': ''},
                      {'username': 'monkey123',
                       'ntlm_hash': '',
                       'password': 'canyoufindme123',
                       'lm_hash': ''},
                      {'username': 'monk3y',
                       'ntlm_hash': '',
                       'password': 'canyoufindm3',
                       'lm_hash': ''},
                      {'username': 'monkey',
                       'ntlm_hash': '',
                       'password': 'canyoufindme2',
                       'lm_hash': ''},
                      {'username': 'monkey@monkey.com',
                       'ntlm_hash': '',
                       'password': 'canyoufindme1',
                       'lm_hash': ''},
                      {'username': 'test',
                       'ntlm_hash': '',
                       'password': 'canyoufindit',
                       'lm_hash': ''},
                      ]
        results = [result.to_dict() for result in results]
        [self.assertTrue(test_dict in results) for test_dict in test_dicts]
