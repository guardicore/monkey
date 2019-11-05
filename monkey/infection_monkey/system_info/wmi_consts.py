WMI_CLASSES = {"Win32_OperatingSystem", "Win32_ComputerSystem", "Win32_LoggedOnUser", "Win32_UserAccount",
               "Win32_UserProfile", "Win32_Group", "Win32_GroupUser", "Win32_Product", "Win32_Service",
               "Win32_OptionalFeature"}

# These wmi queries are able to return data about all the users & machines in the domain.
# For these queries to work, the monkey should be run on a domain machine and
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
