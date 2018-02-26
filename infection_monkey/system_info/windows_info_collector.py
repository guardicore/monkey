import os
import logging
import traceback

import _winreg
from wmi import WMI
#from mimikatz_collector import MimikatzCollector
from . import InfoCollector

LOG = logging.getLogger(__name__)

__author__ = 'uri'

WMI_CLASSES = set(["Win32_OperatingSystem",
                   "Win32_ComputerSystem",
                   "Win32_GroupUser",
                   "Win32_LoggedOnUser",
                   "Win32_UserProfile",
                   "win32_UserAccount",
                   "Win32_Process",
                   "Win32_Product",
                   "Win32_Service"])


class WindowsInfoCollector(InfoCollector):
    """
    System information collecting module for Windows operating systems
    """

    def __init__(self):
        super(WindowsInfoCollector, self).__init__()
        self.wmi = None

    def get_info(self):
        """
        Collect Windows system information
        Hostname, process list and network subnets
        Tries to read credential secrets using mimikatz
        :return: Dict of system information
        """
        LOG.debug("Running Windows collector")
        self.get_hostname()
        self.get_process_list()
        self.get_network_info()
        
        self.get_wmi_info()
        self.get_reg_key(r"SYSTEM\CurrentControlSet\Control\Lsa")
        self.get_installed_packages()
        
        #mimikatz_collector = MimikatzCollector()
        #self.info["credentials"] = mimikatz_collector.get_logon_info()

        return self.info

    def get_installed_packages(self):
        self.info["installed_packages"] = os.popen("dism /online /get-packages").read()
        self.info["installed_features"] = os.popen("dism /online /get-features").read()
        
    def get_wmi_info(self):
        for wmi_class_name in WMI_CLASSES:
            self.info[wmi_class_name] = self.get_wmi_class(wmi_class_name)

    def get_wmi_class(self, class_name):
        if not self.wmi:
            self.wmi = WMI()

        try:
            wmi_class = getattr(self.wmi, class_name)()
        except:
            LOG.error("Error getting wmi class '%s'" % (class_name, ))
            LOG.error(traceback.format_exc())
            return

        result = []
        
        for item in wmi_class:
            row = {}
        
            for prop in item.properties:
                value = getattr(item, prop)
                row[prop] = value

            for method_name in item.methods:
                if not method_name.startswith("GetOwner"):
                    continue

                method = getattr(item, method_name)

                try:
                    row[method_name[3:]] = method()
                    
                except:
                    LOG.error("Error running wmi method '%s'" % (method_name, ))
                    LOG.error(traceback.format_exc())
                    continue

            result.append(row)

        return result

    def get_reg_key(self, subkey_path, store=_winreg.HKEY_LOCAL_MACHINE):
        key = _winreg.ConnectRegistry(None, store)
        subkey = _winreg.OpenKey(key, subkey_path)

        self.info[subkey_path] = [_winreg.EnumValue(subkey, i) for i in xrange(_winreg.QueryInfoKey(subkey)[0])]

        subkey.Close()
        key.Close()