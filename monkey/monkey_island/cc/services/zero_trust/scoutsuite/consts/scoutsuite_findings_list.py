from .scoutsuite_findings import (DataLossPrevention, Logging,
                                  PermissiveFirewallRules,
                                  RestrictivePolicies,
                                  SecureAuthentication, ServiceSecurity,
                                  UnencryptedData)

SCOUTSUITE_FINDINGS = [PermissiveFirewallRules, UnencryptedData, DataLossPrevention, SecureAuthentication,
                       RestrictivePolicies, Logging, ServiceSecurity]
