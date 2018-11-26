import logging
import uuid
from datetime import datetime
import boto3

from cc.resources.exporter import Exporter
from cc.services.config import ConfigService

logger = logging.getLogger(__name__)

AWS_CRED_CONFIG_KEYS = [['cnc', 'aws_config', 'aws_access_key_id'],
                        ['cnc', 'aws_config', 'aws_secret_access_key']]


class AWSExporter(Exporter):

    @staticmethod
    def handle_report(report_json):

        findings_list = []
        issues_list = report_json['recommendations']['issues']
        for machine in issues_list:
            for issue in issues_list[machine]:
                findings_list.append(AWSExporter._prepare_finding(issue))

        if not AWSExporter._send_findings(findings_list, AWSExporter._get_aws_keys()):
            logger.error('Exporting findings to aws failed')
            return False

        return True

    @staticmethod
    def _get_aws_keys():
        creds_dict = {}
        for key in AWS_CRED_CONFIG_KEYS:
            creds_dict[key[2]] = ConfigService.get_config_value(key)

        return creds_dict

    @staticmethod
    def merge_two_dicts(x, y):
        z = x.copy()  # start with x's keys and values
        z.update(y)  # modifies z with y's keys and values & returns None
        return z

    @staticmethod
    def _prepare_finding(issue):
        findings_dict = {
            'island_cross_segment': AWSExporter._handle_island_cross_segment_issue,
            'ssh': AWSExporter._handle_ssh_issue,
            'shellshock': AWSExporter._handle_shellshock_issue,
            'tunnel': AWSExporter._handle_tunnel_issue,
            'elastic': AWSExporter._handle_elastic_issue,
            'smb_password': AWSExporter._handle_smb_password_issue,
            'smb_pth': AWSExporter._handle_smb_pth_issue,
            'sambacry': AWSExporter._handle_sambacry_issue,
            'shared_passwords': AWSExporter._handle_shared_passwords_issue,
        }

        finding = {
            "SchemaVersion": "2018-10-08",
            "Id": uuid.uuid4().hex,
            "ProductArn": "arn:aws:securityhub:us-west-2:324264561773:product/aws/guardduty",
            "GeneratorId": issue['type'],
            "AwsAccountId": "324264561773",
            "Types": [
                "Software and Configuration Checks/Vulnerabilities/CVE"
            ],
            "CreatedAt": datetime.now().isoformat() + 'Z',
            "UpdatedAt": datetime.now().isoformat() + 'Z',
        }
        return AWSExporter.merge_two_dicts(finding, findings_dict[issue['type']](issue))

    @staticmethod
    def _send_findings(findings_list, creds_dict):

        securityhub = boto3.client('securityhub',
                                   aws_access_key_id=creds_dict.get('aws_access_key_id', ''),
                                   aws_secret_access_key=creds_dict.get('aws_secret_access_key', ''))
        import_response = securityhub.batch_import_findings(Findings=findings_list)
        print import_response
        if import_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False

    @staticmethod
    def _handle_tunnel_issue(issue):
        finding =\
            {
                "Severity": {
                    "Product": 5,
                    "Normalized": 100
                },
                "Resources": [{
                    "Type": "IpAddress",
                    "Id": issue['dest']
                }],
                "RecordState": "ACTIVE",
            }

        finding["Title"] = "Weak segmentation - Machines were able to communicate over unused ports."
        finding["Description"] = "Use micro-segmentation policies to disable communication other than the required."
        finding["Remediation"] = {
            "Recommendation": {
                "Text": "Machines are not locked down at port level. Network tunnel was set up from {0} to {1}"
                    .format(issue['machine'], issue['dest'])
            }
        }
        return finding

    @staticmethod
    def _handle_sambacry_issue(issue):
        finding = \
            {
                "Severity": {
                    "Product": 10,
                    "Normalized": 100
                },
                "Resources": [{
                    "Type": "IpAddress",
                    "Id": str(issue['ip_address'])
                }],
                "RecordState": "ACTIVE",
            }

        finding["Title"] = "Samba servers are vulnerable to 'SambaCry'"
        finding["Description"] = "Change {0} password to a complex one-use password that is not shared with other computers on the network. Update your Samba server to 4.4.14 and up, 4.5.10 and up, or 4.6.4 and up."\
            .format(issue['username'])
        finding["Remediation"] = {
            "Recommendation": {
                "Text": "The machine {0} ({1}) is vulnerable to a SambaCry attack. The Monkey authenticated over the SMB protocol with user {2} and its password, and used the SambaCry vulnerability.".format(issue['machine'], issue['ip_address'], issue['username'])
            }
        }
        return finding

    @staticmethod
    def _handle_smb_pth_issue(issue):
        finding = \
            {
                "Severity": {
                    "Product": 5,
                    "Normalized": 100
                },
                "Resources": [{
                    "Type": "IpAddress",
                    "Id": issue['ip_address']
                }],
                "RecordState": "ACTIVE",
            }

        finding["Title"] = "Machines are accessible using passwords supplied by the user during the Monkey's configuration."
        finding["Description"] = "Change {0}'s password to a complex one-use password that is not shared with other computers on the network.".format(issue['username'])
        finding["Remediation"] = {
            "Recommendation": {
                "Text": "The machine {0}({1}) is vulnerable to a SMB attack. The Monkey used a pass-the-hash attack over SMB protocol with user {2}.".format(issue['machine'], issue['ip_address'], issue['username'])
            }
        }
        return finding

    @staticmethod
    def _handle_ssh_issue(issue):
        finding = \
            {
                "Severity": {
                    "Product": 1,
                    "Normalized": 100
                },
                "Resources": [{
                    "Type": "IpAddress",
                    "Id": issue['ip_address']
                }],
                "RecordState": "ACTIVE",
            }

        finding["Title"] = "Machines are accessible using SSH passwords supplied by the user during the Monkey's configuration."
        finding["Description"] = "Change {0}'s password to a complex one-use password that is not shared with other computers on the network.".format(issue['username'])
        finding["Remediation"] = {
            "Recommendation": {
                "Text": "The machine {0} ({1}) is vulnerable to a SSH attack. The Monkey authenticated over the SSH protocol with user {2} and its password.".format(issue['machine'], issue['ip_address'], issue['username'])
            }
        }
        return finding

    @staticmethod
    def _handle_elastic_issue(issue):
        finding = \
            {
                "Severity": {
                    "Product": 10,
                    "Normalized": 100
                },
                "Resources": [{
                    "Type": "IpAddress",
                    "Id": issue['ip_address']
                }],
                "RecordState": "ACTIVE",
            }

        finding["Title"] = "Elasticsearch servers are vulnerable to CVE-2015-1427"
        finding["Description"] = "Update your Elastic Search server to version 1.4.3 and up."
        finding["Remediation"] = {
            "Recommendation": {
                "Text": "The machine {0}({1}) is vulnerable to an Elastic Groovy attack. The attack was made possible because the Elastic Search server was not patched against CVE-2015-1427.".format(issue['machine'], issue['ip_address'])
            }
        }
        return finding

    @staticmethod
    def _handle_island_cross_segment_issue(issue):
        finding = \
            {
                "Severity": {
                    "Product": 1,
                    "Normalized": 100
                },
                "Resources": [{
                    "Type": "IpAddress",
                    "Id": issue['networks'][0][:-2]
                }],
                "RecordState": "ACTIVE",
            }

        finding["Title"] = "Weak segmentation - Machines from different segments are able to communicate."
        finding["Description"] = "egment your network and make sure there is no communication between machines from different segments."
        finding["Remediation"] = {
            "Recommendation": {
                "Text": "The network can probably be segmented. A monkey instance on \
                        {0} in the networks {1} \
                        could directly access the Monkey Island server in the networks {2}.".format(issue['machine'],
                                                                                                    issue['networks'],
                                                                                                    issue['server_networks'])
            }
        }
        return finding

    @staticmethod
    def _handle_shared_passwords_issue(issue):
        finding = \
            {
                "Severity": {
                    "Product": 1,
                    "Normalized": 100
                },
                "Resources": [{
                    "Type": "IpAddress",
                    "Id": '10.0.0.1'
                }],
                "RecordState": "ACTIVE",
            }

        finding["Title"] = "Multiple users have the same password"
        finding["Description"] = "Some users are sharing passwords, this should be fixed by changing passwords."
        finding["Remediation"] = {
            "Recommendation": {
                "Text": "These users are sharing access password: {0}.".format(issue['shared_with'])
            }
        }
        return finding

    @staticmethod
    def _handle_shellshock_issue(issue):
        finding = \
            {
                "Severity": {
                    "Product": 10,
                    "Normalized": 100
                },
                "Resources": [{
                    "Type": "IpAddress",
                    "Id": issue['ip_address']
                }],
                "RecordState": "ACTIVE",
            }

        finding["Title"] = "Machines are vulnerable to 'Shellshock'"
        finding["Description"] = "Update your Bash to a ShellShock-patched version."
        finding["Remediation"] = {
            "Recommendation": {
                "Text": "The machine {0} ({1}) is vulnerable to a ShellShock attack. The attack was made possible because the HTTP server running on TCP port {2} was vulnerable to a shell injection attack on the paths: {3}.".format(issue['machine'], issue['ip_address'], issue['port'], issue['paths'])
            }
        }
        return finding

    @staticmethod
    def _handle_smb_password_issue(issue):
        finding = \
            {
                "Severity": {
                    "Product": 1,
                    "Normalized": 100
                },
                "Resources": [{
                    "Type": "IpAddress",
                    "Id": issue['ip_address']
                }],
                "RecordState": "ACTIVE",
            }

        finding["Title"] = "Machines are accessible using passwords supplied by the user during the Monkey's configuration."
        finding["Description"] = "Change {0}'s password to a complex one-use password that is not shared with other computers on the network."
        finding["Remediation"] = {
            "Recommendation": {
                "Text": "The machine {0} ({1}) is vulnerable to a SMB attack. The Monkey authenticated over the SMB protocol with user {2} and its password.".format(issue['machine'], issue['ip_address'], issue['username'])
            }
        }
        return finding
