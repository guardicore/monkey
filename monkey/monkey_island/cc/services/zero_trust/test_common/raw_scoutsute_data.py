# This is what our codebase receives after running ScoutSuite module.
# Object '...': {'...': '...'} represents continuation of similar objects as above
RAW_SCOUTSUITE_DATA = {
    'sg_map': {
        'sg-abc': {'region': 'ap-northeast-1', 'vpc_id': 'vpc-abc'},
        'sg-abcd': {'region': 'ap-northeast-2', 'vpc_id': 'vpc-abc'},
        '...': {'...': '...'}},
    'subnet_map': {
        'subnet-abc': {'region': 'ap-northeast-1', 'vpc_id': 'vpc-abc'},
        'subnet-abcd': {'region': 'ap-northeast-1', 'vpc_id': 'vpc-abc'},
        '...': {'...': '...'}
    },
    'provider_code': 'aws',
    'provider_name': 'Amazon Web Services',
    'environment': None,
    'result_format': 'json',
    'partition': 'aws',
    'account_id': '125686982355',
    'last_run': {
        'time': '2021-02-05 16:03:04+0200',
        'run_parameters': {'services': [], 'skipped_services': [], 'regions': [], 'excluded_regions': []},
        'version': '5.10.0',
        'ruleset_name': 'default',
        'ruleset_about': 'This ruleset',
        'summary': {'ec2': {'checked_items': 3747, 'flagged_items': 262, 'max_level': 'warning', 'rules_count': 28,
                            'resources_count': 176},
                    's3': {'checked_items': 88, 'flagged_items': 25, 'max_level': 'danger', 'rules_count': 18,
                           'resources_count': 5},
                    '...': {'...': '...'}}},
    'metadata': {
        'compute': {
            'summaries': {'external attack surface': {'cols': 1,
                                                      'path': 'service_groups.compute.summaries.external_attack_surface',
                                                      'callbacks': [
                                                          ['merge', {'attribute': 'external_attack_surface'}]]}},
            '...': {'...': '...'}
        },
        '...': {'...': '...'}
    },

    # This is the important part, which we parse to get resources
    'services': {
        'ec2': {'regions': {
            'ap-northeast-1': {
                'vpcs': {
                    'vpc-abc': {
                        'id': 'vpc-abc',
                        'security_groups': {
                            'sg-abc': {
                                'name': 'default',
                                'rules': {
                                    'ingress': {'protocols': {
                                        'ALL': {'ports': {'1-65535': {'cidrs': [{'CIDR': '0.0.0.0/0'}]}}}},
                                        'count': 1},
                                    'egress': {'protocols': {
                                        'ALL': {'ports': {'1-65535': {'cidrs': [{'CIDR': '0.0.0.0/0'}]}}}},
                                        'count': 1}}
                            }
                        }}},
                '...': {'...': '...'}
            }},
            # Interesting info, maybe could be used somewhere in the report
            'external_attack_surface': {
                '52.52.52.52': {'protocols': {'TCP': {'ports': {'22': {'cidrs': [{'CIDR': '0.0.0.0/0'}]}}}},
                                'InstanceName': 'InstanceName',
                                'PublicDnsName': 'ec2-52-52-52-52.eu-central-1.compute.amazonaws.com'}},
            # We parse these into ScoutSuite security rules
            'findings': {
                'ec2-security-group-opens-all-ports-to-all': {
                    'description': 'Security Group Opens All Ports to All',
                    'path': 'ec2.regions.id.vpcs.id.security_groups'
                            '.id.rules.id.protocols.id.ports.id.cidrs.id.CIDR',
                    'level': 'danger',
                    'display_path': 'ec2.regions.id.vpcs.id.security_groups.id',
                    'items': [
                        'ec2.regions.ap-northeast-1.vpcs.vpc-abc.security_groups'
                        '.sg-abc.rules.ingress.protocols.ALL.ports.1-65535.cidrs.0.CIDR'],
                    'dashboard_name': 'Rules',
                    'checked_items': 179,
                    'flagged_items': 2,
                    'service': 'EC2',
                    'rationale': 'It was detected that all ports in the security group are open <...>',
                    'remediation': None, 'compliance': None, 'references': None},
                '...': {'...': '...'}
            }
        },
        '...': {'...': '...'}
    },
    'service_list': ['acm', 'awslambda', 'cloudformation', 'cloudtrail', 'cloudwatch', 'config', 'directconnect',
                     'dynamodb', 'ec2', 'efs', 'elasticache', 'elb', 'elbv2', 'emr', 'iam', 'kms', 'rds', 'redshift',
                     'route53', 's3', 'ses', 'sns', 'sqs', 'vpc', 'secretsmanager'],
    'service_groups': {'...': {'...': '...'}}
}
