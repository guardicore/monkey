from monkey_island.cc.services.zero_trust.scoutsuite.consts.scoutsuite_finding_maps import (
    DataLossPrevention,
    Logging,
    PermissiveFirewallRules,
    RestrictivePolicies,
    SecureAuthentication,
    ServiceSecurity,
    UnencryptedData,
)

SCOUTSUITE_FINDINGS = [
    PermissiveFirewallRules,
    UnencryptedData,
    DataLossPrevention,
    SecureAuthentication,
    RestrictivePolicies,
    Logging,
    ServiceSecurity,
]
