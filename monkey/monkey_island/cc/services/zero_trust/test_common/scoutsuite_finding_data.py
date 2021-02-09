from monkey_island.cc.models.zero_trust.scoutsuite_finding_details import ScoutSuiteFindingDetails
from monkey_island.cc.models.zero_trust.scoutsuite_rule import ScoutSuiteRule
from monkey_island.cc.services.zero_trust.scoutsuite.consts.scoutsuite_finding_maps import PermissiveFirewallRules, \
    UnencryptedData

SCOUTSUITE_FINDINGS = [
    PermissiveFirewallRules,
    UnencryptedData
]

RULES = [
    ScoutSuiteRule(
        checked_items=179,
        compliance=None,
        dashboard_name='Rules',
        description='Security Group Opens All Ports to All',
        flagged_items=2,
        items=[
            'ec2.regions.eu-central-1.vpcs.vpc-0ee259b1a13c50229.security_groups.sg-035779fe5c293fc72'
            '.rules.ingress.protocols.ALL.ports.1-65535.cidrs.2.CIDR',
            'ec2.regions.eu-central-1.vpcs.vpc-00015526b6695f9aa.security_groups.sg-019eb67135ec81e65'
            '.rules.ingress.protocols.ALL.ports.1-65535.cidrs.0.CIDR'
        ],
        level='danger',
        path='ec2.regions.id.vpcs.id.security_groups.id.rules.id.protocols.id.ports.id.cidrs.id.CIDR',
        rationale='It was detected that all ports in the security group are open, and any source IP address'
                  ' could send traffic to these ports, which creates a wider attack surface for resources '
                  'assigned to it. Open ports should be reduced to the minimum needed to correctly',
        references=[],
        remediation=None,
        service='EC2'
    ),
    ScoutSuiteRule(
        checked_items=179,
        compliance=[{'name': 'CIS Amazon Web Services Foundations', 'version': '1.0.0', 'reference': '4.1'},
                    {'name': 'CIS Amazon Web Services Foundations', 'version': '1.0.0', 'reference': '4.2'},
                    {'name': 'CIS Amazon Web Services Foundations', 'version': '1.1.0', 'reference': '4.1'},
                    {'name': 'CIS Amazon Web Services Foundations', 'version': '1.1.0', 'reference': '4.2'},
                    {'name': 'CIS Amazon Web Services Foundations', 'version': '1.2.0', 'reference': '4.1'},
                    {'name': 'CIS Amazon Web Services Foundations', 'version': '1.2.0', 'reference': '4.2'}],
        dashboard_name='Rules',
        description='Security Group Opens RDP Port to All',
        flagged_items=7,
        items=[
            'ec2.regions.eu-central-1.vpcs.vpc-076500a2138ee09da.security_groups.sg-00bdef5951797199c'
            '.rules.ingress.protocols.TCP.ports.3389.cidrs.0.CIDR',
            'ec2.regions.eu-central-1.vpcs.vpc-d33026b8.security_groups.sg-007931ba8a364e330'
            '.rules.ingress.protocols.TCP.ports.3389.cidrs.0.CIDR',
            'ec2.regions.eu-central-1.vpcs.vpc-d33026b8.security_groups.sg-05014daf996b042dd'
            '.rules.ingress.protocols.TCP.ports.3389.cidrs.0.CIDR',
            'ec2.regions.eu-central-1.vpcs.vpc-d33026b8.security_groups.sg-0c745fe56c66335b2'
            '.rules.ingress.protocols.TCP.ports.3389.cidrs.0.CIDR',
            'ec2.regions.eu-central-1.vpcs.vpc-d33026b8.security_groups.sg-0f99b85cfad63d1b1'
            '.rules.ingress.protocols.TCP.ports.3389.cidrs.0.CIDR',
            'ec2.regions.us-east-1.vpcs.vpc-9e56cae4.security_groups.sg-0dc253aa79062835a'
            '.rules.ingress.protocols.TCP.ports.3389.cidrs.0.CIDR',
            'ec2.regions.us-east-1.vpcs.vpc-002d543353cd4e97d.security_groups.sg-01902f153d4f938da'
            '.rules.ingress.protocols.TCP.ports.3389.cidrs.0.CIDR'],
        level='danger',
        path='ec2.regions.id.vpcs.id.security_groups.id.rules.id.protocols.id.ports.id.cidrs.id.CIDR',
        rationale='The security group was found to be exposing a well-known port to all source addresses.'
                  ' Well-known ports are commonly probed by automated scanning tools, and could be an indicator '
                  'of sensitive services exposed to Internet. If such services need to be expos',
        references=[],
        remediation='Remove the inbound rules that expose open ports',
        service='EC2'
    )
]


def get_scoutsuite_details_dto() -> ScoutSuiteFindingDetails:
    scoutsuite_details = ScoutSuiteFindingDetails()
    scoutsuite_details.scoutsuite_rules.append(RULES[0])
    scoutsuite_details.scoutsuite_rules.append(RULES[1])
    return scoutsuite_details


