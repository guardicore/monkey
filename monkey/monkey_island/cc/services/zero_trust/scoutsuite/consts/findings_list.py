from monkey_island.cc.services.zero_trust.scoutsuite.consts.findings import (DATA_LOSS_PREVENTION, LOGGING,
                                                                             PERMISSIVE_FIREWALL_RULES,
                                                                             RESTRICTIVE_POLICIES,
                                                                             SECURE_AUTHENTICATION, SERVICE_SECURITY,
                                                                             UNENCRYPTED_DATA)

SCOUTSUITE_FINDINGS = [PERMISSIVE_FIREWALL_RULES, UNENCRYPTED_DATA, DATA_LOSS_PREVENTION, SECURE_AUTHENTICATION,
                       RESTRICTIVE_POLICIES, LOGGING, SERVICE_SECURITY]
