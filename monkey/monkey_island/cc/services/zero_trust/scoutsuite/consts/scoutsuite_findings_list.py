from monkey_island.cc.services.zero_trust.scoutsuite.consts.scoutsuite_finding_maps import RestrictivePolicies, \
    SecureAuthentication, DataLossPrevention, UnencryptedData, PermissiveFirewallRules, ServiceSecurity, Logging

SCOUTSUITE_FINDINGS = [PermissiveFirewallRules, UnencryptedData, DataLossPrevention, SecureAuthentication,
                       RestrictivePolicies, Logging, ServiceSecurity]
