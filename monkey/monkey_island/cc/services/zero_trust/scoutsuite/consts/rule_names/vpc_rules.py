from enum import Enum


class VPCRules(Enum):
    # Logging
    SUBNET_WITHOUT_FLOW_LOG = 'vpc-subnet-without-flow-log'

    # Firewalls
    SUBNET_WITH_ALLOW_ALL_INGRESS_ACLS = 'vpc-subnet-with-allow-all-ingress-acls'
    SUBNET_WITH_ALLOW_ALL_EGRESS_ACLS = 'vpc-subnet-with-allow-all-egress-acls'
    NETWORK_ACL_NOT_USED = 'vpc-network-acl-not-used'
    DEFAULT_NETWORK_ACLS_ALLOW_ALL_INGRESS = 'vpc-default-network-acls-allow-all-ingress'
    DEFAULT_NETWORK_ACLS_ALLOW_ALL_EGRESS = 'vpc-default-network-acls-allow-all-egress'
    CUSTOM_NETWORK_ACLS_ALLOW_ALL_INGRESS = 'vpc-custom-network-acls-allow-all-ingress'
    CUSTOM_NETWORK_ACLS_ALLOW_ALL_EGRESS = 'vpc-custom-network-acls-allow-all-egress'
